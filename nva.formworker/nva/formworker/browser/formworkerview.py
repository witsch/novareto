import string
from datetime import datetime, date
from time import strftime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PloneFormGen.interfaces import IPloneFormGenField

from nva.formworker import visitorMessageFactory as _


from App.config import getConfiguration
config = getConfiguration()
configuration = config.product_config.get('formworker', dict())
csvbasepath = configuration.get('basepath')

class IformworkerView(Interface):
    """
    formworker view interface
    """

    def test():
        """ test method"""


class formworkerView(BrowserView):
    """
    formworker browser view
    """
    implements(IformworkerView)

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
        mypath = '%s/%s.csv' %(csvbasepath,self.context.title)
        file = open(mypath, 'a')
        formcontent = self.context.listFolderContents()
        formfields=[]
        for i in formcontent:
            if i.__provides__(IPloneFormGenField):
                fieldcontent = self.request.get(i.id, '')
                #Behandlung unterschiedlicher Arten von Feldtypen aus dem Formgenerator
                if fieldcontent.__class__ in normals:
                    formfields.append(self.request.get(i.id, ''))
                elif fieldcontent.__class__ == list:
                    formfields.append(string.join(fieldcontent, ', '))
                elif fieldcontent.__class__ == bool:
                    if fieldcontent == True:
                        formfields.append('ja')
                    else:
                        formfields.append('nein')
                elif fieldcontent.__class__ == date:
                    formfields.append(fieldcontent.strftime("%d.%m.%Y"))
                elif fieldcontent.__class__ == datetime:
                    formfields.append(fieldcontent.strftime("%d.%m.%Y %H:%M"))
        myline = "%s\r\n" %(string.join(formfields, '\t'))
        myline = myline.decode('utf-8')
        myline = myline.encode('utf-16')
        file.write(myline)
        file.close()
        myredirect = self.context.getThanksPageOverride()
        myurl = "%s/%s" %(self.portal.absolute_url(), myredirect)
        return self.request.response.redirect(myurl)    
