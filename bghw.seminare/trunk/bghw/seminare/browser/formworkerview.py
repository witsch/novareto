# -*- coding: utf-8 -*-
import string
import tempfile
from datetime import datetime, date
from time import strftime
from zope.interface import implements, Interface
from collective.beaker.interfaces import ISession

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PloneFormGen.interfaces import IPloneFormGenField
from bghw.seminare.lib.helpers import mapper
from bghw.seminare.lib.pdfgen import createpdf
from bghw.seminare.lib.mail import sMail
from bghw.seminare import seminareMessageFactory as _


#from App.config import getConfiguration
#config = getConfiguration()
#configuration = config.product_config.get('formworker', dict())
#csvbasepath = configuration.get('basepath')

class IseminarworkerView(Interface):
    """
    seminarworker view interface
    """

    def test():
        """ test method"""


class seminarworkerView(BrowserView):
    """
    seminarworker browser view
    """
    implements(IseminarworkerView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def portal_url(self):
        return getToolByName(self.context, 'portal_url')

    @property
    def mail_host(self):
        return getToolByName(self.context, 'MailHost')

    def __call__(self):
        """
           persistiert die Daten im Cookie,
           ruft die Methode zur Generierung des PDFs auf,
           schreibt eine Mail an Teilnehmer und Veranstalter
        """
        session = ISession(self.request)
        myurl = "%s/%s" %(self.context.absolute_url(), 'seminaranmeldung_dank')
        myform = self.request.form
        if self.context.portal_type == "FormFolder":
            if self.context.forceSSL:
                myurl = myurl.replace('http://', 'https://')

        #Wurden die Daten bereits persistiert? -dann direkt zur Danke-Seite
        if session.get('formdata', {}):
            return self.request.response.redirect(myurl)
    
        #Persistenz fuer Daten
        myform['modification'] = datetime.now().strftime('%d.%m.%Y %H:%M')
        session['formdata'] = myform
        session.save()

        #Generierung PDF
        mytmpfile = tempfile.TemporaryFile()
        daten = mapper(myform)
        pdf = createpdf(mytmpfile, daten)
        mytmpfile.seek(0)
        pdfdata = mytmpfile.read()

        #Schreiben von Mails
        teilnehmer = myform.get('replyto', '')
        subject = "Anmeldung zum Seminar: %s" %myform.get('titel', '')
        ehrung = "geehrter"
        if myform.get('anrede', '') == 'Frau':
            ehrung = u"geehrte"
        text_kunde = u"""
Sehr %s %s %s %s,

dies ist eine automatisch generierte E-Mail, bitte antworten Sie nicht an diese E-Mailadresse!

Vielen Dank für Ihre Seminaranmeldung. Diese E-Mail erhalten Sie als Bestätigung Ihrer Seminaranmeldung bei der BGHW. 
Bitte beachten Sie, dass Sie eine endgültige Bestätigung Ihrer Teilnahme am Seminar durch die BGHW auf dem Postweg 
erhalten. Ein Exemplar Ihrer Anmeldung im PDF-Format erhalten Sie als Anlage zur dieser E-Mail.

Mit freundlichen Grüßen
Ihre Berufsgenossenschaft Handel und Warenlogistik

Hinweis: Bei Rückfragen wenden Sie sich bitte an: ausbildung@bghw.de

        """ %(ehrung, myform.get('anrede', ''), myform.get('akad_titel', ''), myform.get('name', ''))
        text_bghw = u"""Im Anhang zu dieser Mail finden Sie die Seminaranmeldung."""
        mailhost = self.mail_host.smtp_host
        cc = ''
        mailbghw = sMail(mailhost, 'ausbildung@bghw.de', 'bghwportal@bghw.de', cc, subject, 
                         text_bghw, pdfdata, 'seminaranmeldung.pdf')

        if teilnehmer:
            cc = myform.get('e-mail-adresse-der-ansprechperson', '')
            mailkunde = sMail(mailhost, teilnehmer, 'ausbildung@bghw.de', cc, subject, 
                              text_kunde, pdfdata, 'seminaranmeldung.pdf')

        return self.request.response.redirect(myurl)    
