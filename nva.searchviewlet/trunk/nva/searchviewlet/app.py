import string
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

    def checkWebcode(self, suchtext, path):
        pcat = self.portal_catalog
        if path:
            brains = self.portal_catalog(Webcode=suchtext, path=path)
        else:
            brains = self.portal_catalog(Webcode=suchtext)
        url = ''
        if len(brains) == 1:
            url = brains[0].getURL()
        elif len(brains) > 1 and path:
            url = '%s/@@search?Webcode=%s&path=%s' %(self.portal_url, suchtext, path)
        elif len(brains) > 1 and not path:
            url = '%s/@@search?Webcode=%s' %(self.portal_url, suchtext)
        return url

    def render(self):
        suchtext =  self.request.get("SearchableText", "")
        path =  self.request.get("path", "")
        if path:
           string.join(path[:-1], '/')
        if suchtext:
            webcodeurl = self.checkWebcode(suchtext, path)
            if webcodeurl:
                return self.request.response.redirect(webcodeurl)
        url = '%s/@@search?SearchableText=%s' %(self.portal_url, suchtext)
        if path:
            url = '%s/@@search?SearchableText=%s&path=%s' %(self.portal_url, suchtext, path)
        return self.request.response.redirect(url)
