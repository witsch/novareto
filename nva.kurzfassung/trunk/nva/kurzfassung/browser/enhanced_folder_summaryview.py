from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.kurzfassung import kurzfassungMessageFactory as _


class Ienhanced_folder_summaryView(Interface):
    """
    enhanced_folder_summary view interface
    """

    def test():
        """ test method"""


class enhanced_folder_summaryView(BrowserView):
    """
    enhanced_folder_summary browser view
    """
    implements(Ienhanced_folder_summaryView)

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
