# -*- coding: utf-8 -*-
from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish


grok.templatedir('templates')

class Ordering_View(uvcsite.Page):
    grok.context(Interface)
    grok.title('Ordering')

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
                       <th>Bestellnr.</th>
                       <th>Titel</th>
                       <th>Bild</th>
                       <th>Download/Bestellung</th>
                       </tr>
                       </thead>
                       <colgroup>
                       <col width="10%">
                       <col width="40%">
                       <col width="20%">
                       <col width="30%">
                       </colgroup>
                       """
        else:
            theader =  """
                       <thead>
                       <tr>
                       <th>Bestellnr.</th>
                       <th>Titel</th>
                       <th>Download/Bestellung</th>
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
        nr = '<td data-title="Bestellnummer."><p>%s</p></td>' % obj.id
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

        download = '<td data-title="Download/Bestellung" align="left">'
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

    def createZeileFromArtikel(self, obj, objectimages, context):
        """
        Create an row of Download-Table from an MediaFileObject
        """

        row='<tr>'
        nr = '<td data-title="Nr."><p>%s</p></td>' % obj.bestellnummer
        row += nr

        title = '<td data-title="Titel"><p><a class="internal-link" href="%s">%s</a></p>\r\n' % (obj.absolute_url(), obj.title)
        description = ''
        if obj.Description():
            description = '<p class="discreet">%s</p>\r\n' %obj.description
        titdesc=title+description+'</td>'
        row += titdesc

        if objectimages:
            myimage = '<td data-title="Bild">'
            if obj.bild:
                url = obj.absolute_url() + '/@@download/bild/' + obj.bild.filename
                img = '<img width="100" src="%s"/>' % url
                image = '<a href="%s">%s</a>\r\n' %(url, img)
                myimage += image
            myimage += '</td>\r\n'
            row += myimage

        download = '<td data-title="Download" align="left">'
        if obj.fileref and obj.status in [u'lieferbar', u'nur Download']:
            if obj.fileref.to_object.portal_type == 'File':
                size = int(float(obj.fileref.to_object.getFile().get_size())/float(1000))
            else:
                size = obj.fileref.to_object.getFile().size/1000
            icon = obj.fileref.to_object.getFile().content_type.split('/')[1]
            kuerzel = icon.upper()
            filedownload = """<a class="download-link" href="%s/at_download/file">
                              <span class="discreet">(%s, %s KByte)</span></a><br/>""" % (
                                                                                       obj.fileref.to_object.absolute_url(),
                                                                                       kuerzel,
                                                                                       size)
            download += filedownload

        if obj.status == u'lieferbar':
            warenkorb = '<a class="internal-link" href="%s/@@tocard?redirect=%s">In den Warenkorb</a>' % (obj.absolute_url(),
                                                                                                          context.absolute_url(),)
            download += warenkorb

        if obj.status == u'nicht lieferbar':
            n_lieferbar = """Der Artikel ist im Moment leider nicht lieferbar."""
            download += n_lieferbar

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
                     <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (obj.id,
                                                                                                     obj.Title(),
                                                                                                     obj.Description(),
                                                                                                     obj.absolute_url(),)
        else:
            row = """<tr><td data-title="Nr.">%s</td><td data-title="Titel"><p><b>%s</b></p><p class="discreet">%s</p></td> 
                     <td data-title="Download"> 
                     <a class="download-link" target="_blank" href="%s">Dokument</a></td></tr>""" % (obj.id,
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
            if obj.portal_type == "bghw.mediashop.artikel":
                if obj.bild:
                    objectimages = True
            myobjectlist.append(obj)
        table = '<table class="table table-striped">\r\n'
        table += self.createTableHeader(objectimages)
        table += '<tbody>\r\n'
        for obj in myobjectlist:
            if obj.portal_type == 'MediaFile':
                table += self.createZeileFromMF(obj, objectimages)
            elif obj.portal_type == 'bghw.mediashop.artikel':
                table += self.createZeileFromArtikel(obj, objectimages, self.context)
            else:
                table += self.createZeileFromObject(obj, objectimages)
        table += '</tbody>\r\n'
        table += '</table>\r\n'
        self.table = table
        return
