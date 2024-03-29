from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish

from nva.download import downloadMessageFactory as _


class IfiledownloadView(Interface):
    """
    filedownload view interface
    """

    def test():
        """ test method"""


class filedownloadView(BrowserView):
    """
    filedownload browser view
    """
    implements(IfiledownloadView)

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

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

    def icons(self, content_type):
        """Gibt fuer jeden Content-Type den Namen der richtigen Icon-Datei zurueck."""
        #Hier muessen die richtigen Icons aus dem Theme zurueckgegeben werden
        return ''

        if 'pdf' in content_type:
           return 'bg_icons_32x32px_pdf.gif'
        if 'word' in content_type:
           return 'bg_icons_32x32px_word.gif'
        if 'rar' in content_type:
           return 'bg_icons_32x32px_zip.gif'
        if 'x-tar' in content_type or 'x-gtar' in content_type:
           return 'bg_icons_32x32px_zip.gif'
        if 'zip' in content_type:
           return 'bg_icons_32x32px_zip.gif'
        if 'video' in content_type:
           return 'bg_icons_32x32px_film.gif'
        if 'excel' in content_type:
           return 'bg_icons_32x32px_xls.gif'
        return 'document_icon.gif'

    def createZeileFromMF(self, obj, trclass, tdclass):

        row='<tr class="%s">' %trclass
        if self.__name__ == 'filedownload_view':
            if obj.getOrderable():
                checkbox = '<td data-title="Hier klicken"><input type="checkbox" name="auswahl" value="%s"</td>' % obj.UID()
            else:
                checkbox = '<td></td>'
            row += checkbox

        if self.__name__ == 'filedownload_view':
            nr = '<td data-title="Nr."><p>%s</p></td>' % obj.id
            row += nr

        title = '<td data-title="Titel"><p>%s</p>\r\n' % obj.Title()
        description = ''
        if obj.Description():
	    description = '<p class="discreet">%s</p>\r\n' %obj.Description()
        titdesc=title+description+'</td>'
        row += titdesc

        myimage = '<td data-title="Bild">' 
        if obj.getImage():
	    url = obj.absolute_url() + '/image/image_view_fullscreen'
            img = obj.tag(width=150, height=150)
	    image = '<a href="%s">%s</a>\r\n' %(url, img)
	    myimage += image
        myimage += '</td>\r\n'
        row += myimage

        download = '<td data-title="Download" align="left">' 
        if obj.getFile().size > 0:
            icon = obj.getFile().content_type.split('/')[1]
            kuerzel = icon.upper()
            filedownload = """<a class="download-link" href="%s/at_download/file">
                              <span class="discreet">(%s, %s KByte)</span></a>""" % (obj.absolute_url(),
                                                                                     kuerzel,
                                                                                     obj.getFile().size/1000,)
            download += filedownload
        download += '</td>\r\n'
        row += download

        row += '</tr>\r\n'
        return row

    def fileobjects(self):
        """
           Render a table with
           filedata from localfolders.
        """
        #brains = self.context.listFolderContents()
        brains = self.query
        tableclass = 'table table-striped'
        table = '<table class="%s">\r\n' %tableclass
        theader =  """
                   <thead>
		   <tr>
                   <th>Titel</th>
                   <th></th>
                   <th>Download</th>
                   </tr>
		   </thead>
                   """
        if self.__name__ == 'filedownload_view':
            theader =  """
		       <thead>
                       <tr>
                       <th></th>
                       <th>Nr.</th>
                       <th>Titel</th>
                       <th></th>
                       <th>Download</th>
                       </tr>
		       </thead>
                       """
        table += theader
        table += '<tbody>'
        orderbutton = []
        for i in brains:
            i = i.getObject()
            if not IFolderish.providedBy(i):
                if i.portal_type == 'MediaFile':
                    if i.getOrderable():
                        orderbutton.append('1')
                    table += self.createZeileFromMF(i, 'normal', 'normal')
                else:
                    row = """<tr><td class="normal"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                             <td class="normal"></td><td class="normal">
                             <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (i.Title(), 
                                                                                                             i.Description(),
                                                                                                             i.absolute_url(),)
                    if self.__name__ == 'filedownload_view':
                        row = """<tr><td class="normal"></td><td class="normal">%s</td>
                                 <td class="normal"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                                 <td class="normal"></td><td class="download-link">
                                 <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (i.id,
                                                                                                                 i.Title(), 
                                                                                                                 i.Description(),
                                                                                                                 i.absolute_url(),)
                    table += row
                    for x in i.getReferences():
                        if x.portal_type == "MediaFile":
                            if x.getOrderable():
                                orderbutton.append('1')
                            table += self.createZeileFromMF(x, 'sub', 'sub')

        table += '</tbody>'
        table += '</table>'
        orderable = False
        if orderbutton and self.__name__ == 'filedownload_view':
            orderable = True

        return {'orderable':orderable, 'table':table}
