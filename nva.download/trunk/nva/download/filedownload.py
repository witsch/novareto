from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish


grok.templatedir('templates')

class Filedownload_View(uvcsite.Page):
    grok.context(Interface)
    grok.title('Datei-Download')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def refs(self, obj):
        """ returns a list of references """
        refs = obj.getRawRelatedItems()
        brains = self.portal_catalog(UID=refs)
        myrefs = []
        res = []
        for i in brains:
            if i.portal_type not in ['Fragebogen']:
                # build a position dict by iterating over the items once
                positions = dict([(v, i) for (i, v) in enumerate(refs)])
                # We need to keep the ordering intact
                res = list(brains)
                def _key(brain):
                    return positions.get(brain.UID, -1)
                res.sort(key=_key)
        for k in res:
            myrefs.append(k.getObject())
        return myrefs

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
	refs = ''    
	if obj.getReferences('relatesTo'):
	  refs = '<p><b>Weitere Informationen:</b></p><ul>'
	  for i in self.refs(obj):
	    refs += '<li><a class="internal-link" href="%s">%s</a></li>' % (i.absolute_url(), i.title)
	  refs += '</ul>'  
        titdescrefs=title+description+refs+'</td>'
        row += titdescrefs

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
            myobjectlist.append(obj)
        table = '<table class="table table-striped">\r\n'
        table += self.createTableHeader(objectimages)
        table += '<tbody>\r\n'
        for obj in myobjectlist:
            if obj.portal_type == 'MediaFile':
                table += self.createZeileFromMF(obj, objectimages)
            else:
                if obj.portal_type not in ['Folder',]:
                    table += self.createZeileFromObject(obj, objectimages)
        table += '</tbody>\r\n'
        table += '</table>\r\n'
        self.table = table
        return
