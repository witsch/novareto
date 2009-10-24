from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.moderatorenliste import moderatorenlisteMessageFactory as _


class ISearchView(Interface):
    """
    Search view interface
    """

    def test():
        """ test method"""


class SearchView(BrowserView):
    """
    Search browser view
    """
    implements(ISearchView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getResults(self):
        """
        test method
        """
        plz = self.request.get('plz', None)
        if not plz:
            return [obj.getObject() for obj in self.portal_catalog(meta_type="Moderatorenliste")]
        if plz:
            plz = "%s*" %plz
        return [obj.getObject() for obj in self.portal_catalog(plz=plz, meta_type="Moderatorenliste")]
