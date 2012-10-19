import string
from time import strftime, localtime
from datetime import datetime, date
from time import strftime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PloneFormGen.interfaces import IPloneFormGenField

from nva.formworker import visitorMessageFactory as _

class IreportworkerView(Interface):
    """
    reportworker view interface
    """

    def test():
        """ test method"""


class reportworkerView(BrowserView):
    """
    reportworker browser view
    """
    implements(IreportworkerView)

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
    def portal_url(self):
        return getToolByName(self.context, 'portal_url')

    def __call__(self):
        normals = [str, int, float]
        myproject = self.request.get('myproject', '')
        if not myproject:
            return
        brains = self.portal_catalog(portal_type="Project Folder", projectnumber=myproject)
        if not brains:
            return
        folder = brains[0].getObject().getBerichtsordner()
        formcontent = self.context.listFolderContents()
        formfields=[]
        for i in formcontent:
            if i.__provides__(IPloneFormGenField):
                fieldcontent = self.request.get(i.id, '')
                #Behandlung unterschiedlicher Arten von Feldtypen aus dem Formgenerator
                if fieldcontent.__class__ in normals:
                    formfields.append('<h3>%s</h3>' %i.title)
                    if i.description:
                        formfields.append('<p><b>%s</b></p>' %i.description)
                    formfields.append('<p>%s</p>' %self.request.get(i.id, ''))
                elif fieldcontent.__class__ == list:
                    formfields.append('<h3>%s</h3>' %i.title)
                    if i.description:
                        formfields.append('<p><b>%s</b></p>' %i.description)
                    formfields.append('<p>%s</p>' %string.join(fieldcontent, ', '))
                elif fieldcontent.__class__ == bool:
                    formfields.append('<h3>%s</h3>' %i.title)
                    if i.description:
                        formfields.append('<p><b>%s</b></p>' %i.description)
                    if fieldcontent == True:
                        formfields.append('<p>ja</p>')
                    else:
                        formfields.append('<p>nein</p>')
                elif fieldcontent.__class__ == date:
                    formfields.append('<h3>%s</h3>' %i.title)
                    if i.description:
                        formfields.append('<p><b>%s</b></p>' %i.description)
                    formfields.append('<p>%s</p>' %fieldcontent.strftime("%d.%m.%Y"))
                elif fieldcontent.__class__ == datetime:
                    formfields.append('<h3>%s</h3>' %i.title)
                    if i.description:
                        formfields.append('<p><b>%s</b></p>' %i.description)
                    formfields.append('<p>%s</p>' %fieldcontent.strftime("%d.%m.%Y %H:%M"))
        myhtml = string.join(formfields, ' ')
        objid = "report-%s" %strftime('%d-%m-%Y-%H%M%S', localtime())
        folder.invokeFactory(id = objid,
                             type_name = "Document",
                             title = "Report vom: %s" %strftime('%d.%m.%Y', localtime()),
                             text = myhtml)
        myurl = getattr(folder, objid).absolute_url()
        return self.request.response.redirect(myurl)    
