import tempfile
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.beaker.interfaces import ISession
from bghw.seminare.lib.helpers import mapper
from bghw.seminare.lib.pdfgen import createpdf
from bghw.seminare import seminareMessageFactory as _


class IprintView(Interface):
    """
    print view interface
    """

    def test():
        """ test method"""


class printView(BrowserView):
    """
    print browser view
    """
    implements(IprintView)

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
        sorgt fuer den Ausdruck des PDF-Dokuments
        """
        session = ISession(self.request)
        formdata = session.get('formdata', {})
        data = mapper(formdata)
        mytmpfile = tempfile.TemporaryFile()
        createpdf(mytmpfile, data)
        mytmpfile.seek(0)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=seminaranmeldung.pdf')
        return mytmpfile.read()

