from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface

grok.templatedir('templates')

class Filedownload_View(uvcsite.Page):
    grok.context(Interface)
    grok.title('Datei-Download')

    @property
    def query(self):
        """ 
        Make catalog query for the folder listing.
        """
        if IATTopic.providedBy(self.context) or ICollection.providedBy(self.context):
            return self.context.queryCatalog(batch=False)
        elif IFolderish.providedBy(self.context):
            return self.context.getFolderContents(batch=False)

    def createTableHeader(self, objectimages):
        """ Create the Header for Table """
        if objectimages:
            theader =  """
                       <thead>
                       <tr>
                       <th>Nr.</th>
                       <th>Titel</th>
                       <th>Bild</th>
                       <th>Download</th>
                       </tr>
                       </thead>
                       """
        else:
            theader =  """
                       <thead>
                       <tr>
                       <th>Nr.</th>
                       <th>Titel</th>
                       <th>Download</th>
                       </tr>
                       </thead>
                       """
        theader += "\r\n"
        return theader

    def createZeileFromMF(self, obj, objectimages):
        """
        Create an row of Download-Table from an MediaFileObject
        """

        row='<tr>'
        nr = '<td data-title="Nr."><p>%s</p></td>' % obj.id
        row += nr

        title = '<td data-title="Titel"><p>%s</p>\r\n' % obj.Title()
        description = ''
        if obj.Description():
            description = '<p class="discreet">%s</p>\r\n' %obj.Description()
        titdesc=title+description+'</td>'
        row += titdesc

        if objectimages:
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

    def createZeileFromObject(self, obj, objectimages):
        """
        Create a row for Download-View from any other object
        """
        if objectimages:
            row = """<tr><td data-title="Nr.">%s</td><td data-title="Titel"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                     <td data-title="Bild">kein Bild vorhanden</td><td data-title="Download">
                     <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (obj.id
                                                                                                     obj.Title(),
                                                                                                     obj.Description(),
                                                                                                     obj.absolute_url(),)
        else:
            row = """<tr><td data-title="Nr.">%s</td><td data-title="Titel"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                     <td data-title="Download"> 
                     <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (obj.id
                                                                                                     obj.Title(),
                                                                                                     obj.Description(),
                                                                                                     obj.absolute_url(),)
        row += "\r\n"
        return row

    def update(self):
        """
        Render a table for Download-View
        """
        brains = self.query
        myobjectlist = []
        objectimages = False
        for i in brains:
            obj = i.getObject()
            if obj.portal_type == "MediaFile":
                if obj.getImage():
                    objectimages = True
            myobjectlist.append(obj)
        table = '<table class="table table-striped>\r\n'
        table += self.createTableHeader(objectimages)
        table += '<tbody>\r\n'
        for obj in myobjectlist:
            if obj.portal_type == 'MediaFile':
                table += self.createTableFromMF(obj, objectimages)
            else:
                table += self.createTableFromObject(obj, objectimages)
        table += '</tbody>\r\n'
        table += '</table>\r\n'
        self.table = table
        return
