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
from plone.dexterity.content import Container
from bghw.mediashop.interfaces import IArtikelListe, IBestellung
from zope.component.interfaces import IFactory

def getSessionCookie(context):
    """
    Liest das SessionCookie
    """
    session = context.session_data_manager.getSessionData()
    cart_default = {} #leere Artikelliste
    cookie = session.get('cart', cart_default)
    return cookie

def setSessionCookie(context, cookie):
    """
    Schreibt das Cookie in die Session
    """
    print cookie
    session = context.session_data_manager.getSessionData()
    session.set('cart', cookie)

class ToCard(grok.View):
    """View-Klasse um Daten in die Session zu schreiben"""
    grok.context(Interface)

    def update(self):
        cookie = getSessionCookie(self.context)
        if not cookie.has_key(self.context.artikelnummer):
            cookie[self.context.artikelnummer] = {'artikel':self.context, 'menge':1}
            setSessionCookie(self.context, cookie)
        else:
            menge = cookie[self.context.artikelnummer]['menge']
            menge += 1
            cookie[self.context.artikelnummer] = {'artikel':self.context, 'menge':menge}
            setSessionCookie(self.context, cookie)

    def render(self):
        return

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
    grok.implements(IArtikelListe)
    #grok.title = "Raumschild drucken"

    def update(self):
        self.label = "Bestellformular"
        cookie = getSessionCookie(self.context)
        mydefault = []
        for i in cookie:
            mydefault.append(Order(artikel = i,
                                   beschreibung = cookie[i]['artikel'].title,
                                   anzahl = cookie[i]['menge']))
        self.fields.get('bestellung').defaultValue = mydefault

    @uvcsite.action('bestellen')
    def handle_send(self):
        data, errors = self.extractData()
        if errors:
            return
        print data
        #params = urllib.urlencode(data)
        #myurl = self.request.getURL() + '?' + params
        #return self.redirect(myurl)

