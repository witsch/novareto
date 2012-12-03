import string
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.app.uuid.utils import uuidToObject
from nva.bildnachweis import bildnachweisMessageFactory as _


class IimagessummaryView(Interface):
    """
    imagessummary view interface
    """

    def test():
        """ test method"""


class imagessummaryView(BrowserView):
    """
    imagessummary browser view
    """
    implements(IimagessummaryView)

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
    def reference_catalog(self):
        return getToolByName(self.context, 'reference_catalog')

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

    def getSummary(self):
        """
        Sammelt die Daten fuer eine Zusammenfassung.
        """
        image_brains = self.portal_catalog.searchResults(portal_type = 'Image',
                                                         sort_on = 'sortable_title',
                                                         sort_order = 'asc',)
        images = []
        for i in image_brains:
            obj = i.getObject()
            img = {}
            img['title'] = obj.title
            img['url'] = obj.absolute_url() + '/image_view_fullscreen'
            img['thumb'] = obj.tag(scale='thumb')
            img['rights'] = obj.Rights()
            img['contributors'] = string.join(obj.Contributors(), ',')
            img['creators'] = obj.Creators()
            refs_brains = self.reference_catalog(targetUID = i.UID)
            refs = []
            for k in refs_brains:
                ref = {}
                obj = uuidToObject(k.sourceUID)
                ref['title'] = obj.title
                ref['url'] = obj.absolute_url()
                refs.append(ref)
            img['refs'] = refs
            images.append(img)
        return images 
