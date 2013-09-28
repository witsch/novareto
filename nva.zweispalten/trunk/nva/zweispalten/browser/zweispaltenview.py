from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish

from nva.zweispalten import zweispaltenMessageFactory as _


class IzweispaltenView(Interface):
    """
    zweispalten view interface
    """

    def folderitems():
        """ method to query the folder contents """

    def haupttext():
        """ Gibt den Haupttext des Ordners zurueck falls vorhanden """

class zweispaltenView(BrowserView):
    """
    zweispalten browser view
    """
    implements(IzweispaltenView)

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
    def query(self):
        """ 
        Make catalog query for the folder listing.
        """
        if IATTopic.providedBy(self.context) or ICollection.providedBy(self.context):
            return self.context.queryCatalog(batch=False)
        elif IFolderish.providedBy(self.context):
            return self.context.getFolderContents(batch=False)

    def haupttext(self):
        """
        Gibt den Haupttext des Ordners zurueck falls vorhanden
        """
        if self.context.getField('text'):
            return self.context.getField('text').get(self.context)
        return None

    def folderitems(self):
        """ method to query the folder contents """
        content = [item.getObject() for item in self.query] 
        objlist = []
        for obj in content:
            item = {}
            imagelist = []
            #imageCaption = ''
            if obj.portal_type in ['Folder', 'Document', 'Topic', 'Collection'] and getattr(obj, 'spalte', False):
               refs = obj.getReferences('rel_titleimages')
               for ref in refs:
                   imagelist.append(ref.getField('image').tag(ref, scale='mini'))
            item['images'] = imagelist
            item['url'] = obj.absolute_url()
            item['tit'] = obj.title
            item['desc'] = obj.Description
            item['imagecaption'] = ''
            objlist.append(item)
        return objlist
