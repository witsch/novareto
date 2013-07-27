from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

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
                checkbox = '<td class="%s"><input type="checkbox" name="auswahl" value="%s"</td>' %(tdclass, obj.UID())
            else:
                checkbox = '<td class="%s"></td>' % tdclass
            row += checkbox

        if self.__name__ == 'filedownload_view':
            nr = '<td class="%s" ><p>%s</p></td>' % (tdclass, obj.id)
            row += nr

        title = '<td class="%s"><p>%s</p>\r\n' % (tdclass, obj.Title())
        description = ''
        if obj.Description():
	    description = '<p class="discreet">%s</p>\r\n' %obj.Description()
        titdesc=title+description+'</td>'
        row += titdesc

        myimage = '<td class="%s">' %tdclass
        if obj.getImage():
	    url = obj.absolute_url() + '/image/image_view_fullscreen'
            img = obj.tag(width=150, height=150)
	    #img = obj.getField('image').tag(obj, title=obj.getImageCaption(), css_class='tileImage', width=200, height=200)
	    image = '<a href="%s">%s</a>\r\n' %(url, img)
	    myimage += image
        myimage += '</td>\r\n'
        row += myimage

        download = '<td align="left" class="%s">' %tdclass
        if obj.getFile().size > 0:
            icon = self.icons(obj.getFile().content_type)
            filedownload = """<a href="%s/at_download/file">
                              <img src="%s"><br><p class="discreet">%s KByte</p></a>""" % (obj.absolute_url(),
                                                                                           icon,
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
        brains = self.context.listFolderContents()
        tableclass = 'table table-striped'
        table = '<table class="%s">\r\n' %tableclass
        theader =  """
                   <tr>
                   <th>Titel</th>
                   <th></th>
                   <th>Download</th>
                   </tr>
                   """
        if self.__name__ == 'filedownload_view':
            theader =  """
                       <tr>
                       <th></th>
                       <th>Nr.</th>
                       <th>Titel</th>
                       <th></th>
                       <th>Download</th>
                       </tr>
                       """
        table += theader
        orderbutton = []
        for i in brains:
            if not i.restrictedTraverse('@@plone').isStructuralFolder():
                if i.portal_type == 'MediaFile':
                    if i.getOrderable():
                        orderbutton.append('1')
                    table += self.createZeileFromMF(i, 'normal', 'normal')
                else:
                    row = """<tr><td class="normal"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                             <td class="normal"></td><td class="normal"><a href="%s">Hinweise</a></td></tr>""" % (i.Title(), 
                                                                                                                 i.Description(),
                                                                                                                 i.absolute_url(),)
                    if self.__name__ == 'filedownload_view':
                        row = """<tr><td class="normal"></td><td class="normal">%s</td>
                                 <td class="normal"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                                 <td class="normal"></td><td class="normal"><a href="%s">Hinweise</a></td></tr>""" % (i.id,
                                                                                                                 i.Title(), 
                                                                                                                 i.Description(),
                                                                                                                 i.absolute_url(),)
                    table += row
                    for x in i.getReferences():
                        if x.portal_type == "MediaFile":
                            if x.getOrderable():
                                orderbutton.append('1')
                            table += self.createZeileFromMF(x, 'sub', 'sub')

        table += '</table>'
        orderable = False
        if orderbutton and self.__name__ == 'filedownload_view':
            orderable = True

        return {'orderable':orderable, 'table':table}
