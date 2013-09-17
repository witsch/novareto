from zope.interface import Interface
from uvc.api import api
from uvc.api.api import grok
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.interfaces import IPortalHeader

grok.templatedir('templates')

class NvaSearchViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IPortalHeader)

class NvaSearch(api.Page):
    grok.context(Interface)
    grok.title('Suche')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_url(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url() 

    def checkWebcode(self, suchtext):
        pcat = self.portal_catalog
        brains = self.portal_catalog(Webcode=suchtext)
        url = ''
        if len(brains) == 1:
            url = brains[0].getURL()
        elif len(brains) > 1:
            url = '%s/@@search?Webcode=%s' %(self.portal_url, suchtext)
        return url

    def render(self):
        suchtext =  self.request.get("SearchableText", "")
        if suchtext:
            webcodeurl = self.checkWebcode(suchtext)
            if webcodeurl:
                return self.request.response.redirect(webcodeurl)
        url = '%s/@@search?SearchableText=%s' %(self.portal_url, suchtext)
        return self.request.response.redirect(url)
