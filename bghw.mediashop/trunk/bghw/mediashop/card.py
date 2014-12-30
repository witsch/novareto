# -*- coding: utf-8 -*-
from five import grok
from uvc.api import api as uvcsite
from zope import schema
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from zope.schema.vocabulary import SimpleVocabulary
from zeam.form.plone import Form
from zeam.form.base import Fields, action
from zeam.form.base.markers import Marker
from plone.dexterity.content import Container
from zope.component.interfaces import IFactory
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from collective.beaker.interfaces import ISession
from bghw.mediashop.interfaces import IArtikelListe, IBestellung
from bghw.mediashop.lib.mailer import createMessage, createOrderMessage
from bghw.mediashop.lib.service import addToWS

grok.templatedir('card_templates')

def getSessionCookie(context, request):
    """
    Liest das SessionCookie
    """
    #session = context.session_data_manager.getSessionData()
    session = ISession(request)
    cart_default = {} #leere Artikelliste
    cookie = session.get('cart', cart_default)
    return cookie

def setSessionCookie(context, cookie, request):
    """
    Schreibt das Cookie in die Session
    """
    #session = context.session_data_manager.getSessionData()
    #session.set('cart', cookie)
    session = ISession(request)
    session['cart'] = cookie
    session.save()

class ToCard(grok.View):
    """View-Klasse um Daten in die Session zu schreiben"""
    grok.context(Interface)

    def update(self):
        cookie = getSessionCookie(self.context, self.request)
        if not cookie.has_key(self.context.artikelnummer):
            cookie[self.context.artikelnummer] = {'artikel':self.context.title, 'bestellung':self.context.bestellnummer, 'menge':1}
            setSessionCookie(self.context, cookie, self.request)
        else:
            menge = cookie[self.context.artikelnummer]['menge']
            menge += 1
            cookie[self.context.artikelnummer] = {'artikel':self.context.title, 'bestellung': self.context.bestellnummer, 'menge':menge}
            setSessionCookie(self.context, cookie, self.request)

    def render(self):
        url = self.request.get('redirect')
        return self.request.response.redirect(url)

class DelCard(grok.View):
    """View-Klasse um die Daten des Cookies zu loeschen"""
    grok.context(Interface)

    def update(self):
        #session = self.context.session_data_manager.getSessionData()
        session = ISession(self.request)
        del session['cart']
        session.save()

    def render(self):
        url = self.request.get('redirect')
        return self.request.response.redirect(url)

class Order(Container):
    """Objekt fuer die Artikelliste der Bestellung"""
    grok.implements(IArtikelListe)

class OrderFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('bghw.mediashop.interfaces.IArtikelListe')

    def __call__(self, **kw):
        return  Order(**kw)

class medienBestellung(uvcsite.Form):
    """Form fuer die Bestellung"""
    grok.context(Interface)
    fields = Fields(IBestellung)
    fields['hinweis'].mode = "radio"
    grok.implements(IArtikelListe)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def update(self):
        #Lesen des Cookies aus der Session
        cookie = getSessionCookie(self.context, self.request)

        #Loeschen von Artikeln in der Session wenn im Formular geloescht wird
        if self.request.form.get('form.field.bestellung.remove'):
            requestkeys = self.request.keys()
            for i in requestkeys:
                if i.startswith('form.field.bestellung.checked'):
                    fieldid = i.split('.')[-1]
                    delart = self.request.get('form.field.bestellung.field.%s.field.artikel' %fieldid)
                    del cookie[delart]
            setSessionCookie(self.context, cookie, self.request)
            if not cookie:
                return self.request.response.redirect(self.context.absolute_url())

        #Setzen der Accordion-Klassen
        self.collapseOne = 'row accordion-body in collapse'
        self.collapseTwo = 'accordion-body collapse'
        if self.request.form.get('form.action.bestellen') == 'bestellen':
            self.collapseOne = 'row accordion-body in collapse'
            self.collapseTwo = 'accordion-body in collapse'

        #Default - Belegung des Formularfeldes Bestellung
        mydefault = []
        for i in cookie:
            mydefault.append(Order(artikel = i,
                                   bestellnummer = cookie[i]['bestellung'],
                                   beschreibung = cookie[i]['artikel'],
                                   anzahl = cookie[i]['menge']))
        self.fields.get('bestellung').defaultValue = mydefault

    def finalizeOrder(self, data):
        mailhost = getToolByName(self.context, 'MailHost')
        mailfrom = 'medien@bghw.de'
        mailto = data.get('email')
        try:
            bestellnummer = addToWS(data)
        except:
            bestellnummer = None
        print bestellnummer
        #Versand der Bestellung an den Kunden
        message = createMessage(data, bestellnummer)
        message = message.encode('utf-8')
        betreff = u'Neue Bestellung aus dem BGHW-Mediashop'
        mailhost.send(message, mto=mailto, mfrom=mailfrom, subject=betreff, charset='utf-8')
        #Versand der Bestellung an die Medienverwaltung
        message = createOrderMessage(data, bestellnummer)
        message = message.encode('utf-8')
        mailhost.send(message, mto='medien@bghw.de', mfrom=self.portal.email_from_address, subject=betreff, charset='utf-8')

    @uvcsite.action('bestellen')
    def handle_send(self):
        data, errors = self.extractData()
        if errors:
            return
        self.finalizeOrder(data)
        redirect = self.context.absolute_url() + '/@@thankyouview'
        url = self.context.absolute_url() + '/@@delcard'
        url = '%s?redirect=%s' % (url, redirect)
        return self.request.response.redirect(url)
        #params = urllib.urlencode(data)
        #myurl = self.request.getURL() + '?' + params
        #return self.redirect(myurl)

class My_Fields(grok.View):
    grok.context(Interface)

class ThankYouView(uvcsite.Page):
    grok.context(Interface)

