from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.galleryview import galleryviewMessageFactory as _


class IdocumentgalleryView(Interface):
    """
    documentgallery view interface
    """

    def test():
        """ test method"""


class documentgalleryView(BrowserView):
    """
    documentgallery browser view
    """
    implements(IdocumentgalleryView)

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

    def mygallery(self):
        """
        returns a gallery_view
        """
        images=[]
        related=[]
        for i in self.context.getReferences():
            if i.portal_type == 'Image':
                image = {}
                image['myhref'] = i.absolute_url()
                image['mythumb'] = i.absolute_url()+'/image_thumb'
                image['mylongdesc'] = i.absolute_url()
                image['mytitle'] = i.title
                images.append(image)
            else:
                related.append(i)
        attachments = {'images':images, 'related':related}
        return attachments

