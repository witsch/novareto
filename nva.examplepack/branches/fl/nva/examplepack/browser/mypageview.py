from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.examplepack import examplepackMessageFactory as _


class ImypageView(Interface):
    """
    mypage view interface
    """

    def test():
        """ test method"""


class mypageView(BrowserView):
    """
    mypage browser view
    """
    implements(ImypageView)

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
    
    def meinefamilie(self):
        """
        gibt eine Liste an den Browser
        """
        meinefamilie = ['Anke', 'Axel', 'Franz', 'Luisa']
        return meinefamilie
        
    def meinedaten(self):
        """
        gibt ein Dictionary an den Browser
        """
        meinedaten = {'franz':{'groesse':1.75, 'alter':15, 'klasse':9, 'ort':'Wilhermsdorf'}}
        return meinedaten        
