import string
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
        mypath = '%s/%s.csv' %(csvbasepath,self.context.title)
        file = open(mypath, 'a')
        formcontent = self.context.listFolderContents()
        formfields=[]
        for i in formcontent:
            if i.__provides__(IPloneFormGenField):
                formfields.append(self.request.get(i.id, ''))
        myline = "%s\r\n" %(string.join(formfields, ';'))
        file.write(myline)
        file.close()
        myredirect = self.context.getThanksPageOverride()
        myurl = "%s/%s" %(self.portal.absolute_url(), myredirect)
        return self.request.response.redirect(myurl)    

