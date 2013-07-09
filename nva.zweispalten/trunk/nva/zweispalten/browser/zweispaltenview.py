from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.zweispalten import zweispaltenMessageFactory as _


class IzweispaltenView(Interface):
    """
    zweispalten view interface
    """

    def folderitems():
        """ method to query the folder contents """


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

    def folderitems(self):
        """ method to query the folder contents """

        topimage = None
        titelbilder = self.context.getReferences('rel_titleimages')
        if getattr(self.context, 'anzeige', False):
            if titelbilder:
                topimage = titelbilder[0].getField('folderimage').tag(self.context, scale='mini')
            #if getattr(self.context, 'imageCaption', None):
            #    imagecaption = self.context.getField('imageCaption').get(self.context)

        ret = {'top':topimage,
               'tit':self.context.Title(),
               'desc':self.context.Description(),
               'topcaption':'',
              }
       
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
            item['desc'] = brain.Description
            item['imagecaption'] = ''
            objlist.append(item)
            #if brain.portal_type != 'Folder':
            #    objlist.append(item)
            #elif brain.portal_type == 'Folder':
            #    if not getattr(brain.aq_explicit, 'exclude_from_nav'):
            #        objlist.append(item)
    
        ret['folderobjects'] = objlist
        return ret
