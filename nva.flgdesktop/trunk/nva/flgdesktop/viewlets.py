from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from plone.app.layout.viewlets.interfaces import IBelowContentBody
from nva.onlinetest.interfaces import Imyfernlehrgang

grok.templatedir('templates')

class DownloadWoid_Viewlet(grok.Viewlet):
    grok.context(Imyfernlehrgang)
    grok.viewletmanager(IBelowContentBody)

    def query(self, context):
        """ 
        Make catalog query for the folder listing.
        """
        if IATTopic.providedBy(context) or ICollection.providedBy(context):
            return context.queryCatalog(batch=False)
        elif IFolderish.providedBy(context):
            return context.getFolderContents(batch=False)

    def createTableHeader(self, objectimages):
        """ Create the Header for Table """
        if objectimages:
            theader =  """
                       <thead>
                       <tr>
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
        title = '<td data-title="Titel"><p><a href="%s">%s</a></p>\r\n' % (obj.absolute_url(), obj.Title())
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
            row = """<tr><td data-title="Titel"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                     <td data-title="Bild">kein Bild vorhanden</td><td data-title="Download">
                     <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (obj.Title(),
                                                                                                     obj.Description(),
                                                                                                     obj.absolute_url(),)
        else:
            row = """<tr><td data-title="Titel"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                     <td data-title="Download"> 
                     <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (obj.Title(),
                                                                                                     obj.Description(),
                                                                                                     obj.absolute_url(),)
        row += "\r\n"
        return row

    def update(self):
        """
        Render a table for Download-View
        """
        lehrhefte = self.context.getLehrhefte()
        brains = []
        if lehrhefte:
            brains = self.query(lehrhefte)
        myobjectlist = []
        objectimages = False
        for i in brains:
            obj = i.getObject()
            if obj.portal_type == "MediaFile":
                if obj.getImage():
                    objectimages = True
            myobjectlist.append(obj)
        table = '<table class="table table-striped">\r\n'
        table += self.createTableHeader(objectimages)
        table += '<tbody>\r\n'
        for obj in myobjectlist:
            if obj.portal_type == 'MediaFile':
                table += self.createZeileFromMF(obj, objectimages)
            else:
                table += self.createZeileFromObject(obj, objectimages)
        table += '</tbody>\r\n'
        table += '</table>\r\n'
        self.table = table
        return
