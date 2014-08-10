import tempfile
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from uv.bsbetreuung import bsbetreuungMessageFactory as _
from uv.bsbetreuung.lib.pdfgen import createpdf
from collective.beaker.interfaces import ISession
from pymongo import MongoClient
from bson.objectid import ObjectId

class IbsbprintView(Interface):
    """
    bsbprint view interface
    """

    def __call__():
        """ PDF-Ausdruck """


class bsbprintView(BrowserView):
    """
    bsbprint browser view
    """
    implements(IbsbprintView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def __call__(self):
        """
        Es werden die Daten fuer die Druckaufbereitung gelesen und an den Browser
        uebergeben.
        """
        langvar = self.request.get('LANGUAGE', 'de')

        session = ISession(self.request)
        ma = session.get('start', {})
        gb = session.get('gb', {})
        mongo_objid = session.get('sb', '')
        client = MongoClient('localhost', 27017)
        db = client.bsb_database
        collection = db.bsb_collection
        sb = collection.find_one({"_id":ObjectId(mongo_objid)})

        if not ma or not sb:
            self.context.plone_utils.addPortalMessage(_(u'Leider sind Ihre Angaben zur Online-Handlungshilfe nicht mehr gueltig, bitte versuchen Sie es erneut.'), 'error')
            return self.request.response.redirect(self.portal.absolute_url())

        tmpfile = tempfile.TemporaryFile()
        createpdf(self.context, tmpfile, ma, gb, sb, langvar)

        tmpfile.seek(0)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=onlinehandlungshilfe.pdf')
        return tmpfile.read()

