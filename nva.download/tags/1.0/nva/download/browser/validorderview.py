# -*- coding: utf-8 -*-

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from nva.download import downloadMessageFactory as _

class IvalidorderView(Interface):
    """
    validorder view interface
    """

    def test():
        """ test method"""


class validorderView(BrowserView):
    """
    validorder browser view
    """
    implements(IvalidorderView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}


    def ordermail(self, firma, zhd, strnr, plzort, email, mnr, sonstiges, choices):
        absender = 'website@bgetem.de'
        empfaenger = 'versand@bgetem.de'
        mhost = self.portal.MailHost
        message = u"""
        From: %s
        To: %s
        Subject: Ein Benutzer bestellt Medien der Website

        Firma: %s
        z.Hd. von: %s
        Strasse: %s
        PLZ / Ort: %s
        E-Mail: %s
        Migliedsnummer bei der BGETEM: %s
        Zusätzliche Angaben:s
        %s

        Bestellte Artikel:
        """
        msg = message % (
              absender,
              empfaenger,
              firma.decode('utf-8'), 
              zhd.decode('utf-8'), 
              strnr.decode('utf-8'), 
              plzort.decode('utf-8'), 
              email.decode('utf-8'), 
              mnr.decode('utf-8'), 
              sonstiges.decode('utf-8'))

        artikel = u''
        for i in choices:
            brains = self.portal_catalog.searchResults(UID = i)
            id = brains[0].getObject().id
            titel = brains[0].getObject().title.decode('utf-8')
            art = u'%s x %s (%s) \r\n' % (choices[i], id, titel)
            artikel += art

        msg += artikel

        subject = "Ein Benutzer bestellt Medien der Website"
        subject = subject.encode('iso-8859-15')
        try:
            msg = msg.encode('iso-8859-15')
        except:
            msg = msg
        mhost.send(msg, empfaenger, absender, subject)

    def __call__(self):

        if self.request.get('abbrechen', ''):
            url = self.context.absolute_url()
            IStatusMessage(self.request).addStatusMessage(_(u"Abbruch des Bestellvorgangs."), type="info")
            self.request.response.redirect(url)

        elif self.request.get('bestellen', ''):
            firma = self.request.get('firma', '')
            zhd = self.request.get('zhd', '')
            strnr = self.request.get('strnr', '')
            plzort = self.request.get('plzort','')
            email = self.request.get('email','')
            mnr = self.request.get('mnr','')
            sonstiges = self.request.get('sonstiges','')
            choice = self.request.get('choice','')
            choices = {}
            if choice:
                for i in choice.split('#'):
                    choices[i] = self.request.get(i, '')
            self.ordermail(firma, zhd, strnr, plzort, email, mnr, sonstiges, choices)
            IStatusMessage(self.request).addStatusMessage(_(u"Vielen Dank für Ihre Bestellung. Sie erhalten in den nächsten Tagen Post von uns."), type="info")
            url = self.context.absolute_url()
            return self.request.response.redirect(url)
