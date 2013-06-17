import transaction
import random
import jsonlib2
import StringIO
from time import strftime, localtime
from DateTime import DateTime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.webcodeproxy import webcodeproxyMessageFactory as _


class IgetwebcodeView(Interface):
    """
    getwebcode view interface
    """
    def __call__():
        """ gibt dem externen System einen Webcode zurueck """

class getwebcodeView(BrowserView):
    """
    Webservice API fuer die Ausstellung von Webcodes an externe Systeme
    """
    implements(IgetwebcodeView)

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
    def genWebcode(self):
        """Generiert einen eindeutigen Webcode fuer das System
        Das soll durch folgende Methode erreicht werden:
        * Verkettung 2-stellige Jahreszahl(Konstante) + 6-stellige Zufallszahl
        * Catalogabfrage, ob im betr. Jahr ein Objekt mit dieser Kombination vorhanden ist, wenn ja:
          * wiederholter Aufruf des Zusfallszahlengenerators. """
        aktuell = str(DateTime()).split(' ')[0]
        neujahr = '%s/01/01' %str(DateTime()).split(' ')[0][:4]
        konstante = str(aktuell[2:4])
        zufallszahl = str(random.randint(100000, 999999))
        code = konstante+zufallszahl
        pcat = self.portal_catalog
        results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
        extcodes = self.context.getWebcodes()
        if code in extcodes:
            results.append(code)
        while results:
            zufallszahl=str(random.randint(100000, 999999))
            code=konstante+zufallszahl
            results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
            if code in extcodes:
                results.append(code)
        return code

    def checkSystem(self, system):
        """Prueft, ob die angegebene System-ID hinterlegt ist"""
        systems = self.context.getExtsystems()
        if system in systems:
            return True
        return False

    def writeCodeToProxyObject(self, code):
        """Schreibt den Webcode in das Datenobjekt, um diese Angabe dauerhaft zu 
           speichern"""
        webcodes = list(self.context.getWebcodes())
        webcodes.append(code)
        self.context.setWebcodes(webcodes)
        transaction.commit()
        self.context.reindexObject()

    def createXMLResponse(self, status, error, code):
        """Generiert einen XML-Datensatz fuer die Rueckgabe an den Client"""
        xml = u"""<?xml version="1.0"?>
                  <nvawebcodeproxy>
                    <status>%s</status>
                    <errormessage>%s</errormessage>
                    <webcodes>
                      <webcode>%s</webcode>
                    </webcodes>
                  </nvawebcodeproxy>""" %(status, error, code)
        return xml

    def createJsonResponse(self, status, error, code):
        """Generiert einen JSON-Payload fuer die Rueckgabe an den Client"""
        dict = {'status':status,
                'errormessage':error,
                'webcodes':(code,)
               }
        payload = jsonlib2.write(dict)
        return payload

    def __call__(self, system='', format=''):
        """Gibt den Webcode nach Pruefung der Voraussetzungen an das externe
           System zurueck."""
        status = "success"
        error = ""
        code = ""
        if not system or not self.checkSystem(system):
            error = u"Error: System-ID fehlt oder ist nicht korrekt."
            status = u"error"
        try:
            code = self.genWebcode
            self.writeCodeToProxyObject(code)
        except:
            error = u"Error: Fehler beim Generieren des Webcodes."
            status = u"error"

        if format == 'xml':
            rawxml = self.createXMLResponse(status, error, code)
            RESPONSE = self.request.response
            RESPONSE.setHeader('content-type', 'application/pdf')
            RESPONSE.setHeader('content-disposition', 'attachment; filename=webcode.xml')
            return rawxml
   
        if format == 'json':
            rawjson = self.createJsonResponse(status, error, code)
            RESPONSE = self.request.response
            RESPONSE.setHeader('content-type', 'application/json')
            RESPONSE.setHeader('content-disposition', 'attachment; filename=webcode.json')
            return rawjson

        if not format and status == "error":
            return error

        if not format and status == "success":
            return code

        return u"Error: Angabe zum Format ist nicht gueltig."
