import string
import urllib
from zope.interface import Interface
from uvc.api import api
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.interfaces import IPortalHeader
from zope.component import queryUtility
try:
    from collective.solr.interfaces import ISolrConnectionConfig
except:
    ISolrConnectionConfig = None

api.templatedir('templates')

class NvaSearchViewlet(api.Viewlet):
    api.context(Interface)
    api.viewletmanager(IPortalHeader)

class NvaSearch(api.Page):
    api.context(Interface)
    api.title('Suche')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_url(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url() 

    def VedaIframe(self, url):
        """prueft, ob die URL eventuell umgesetzt werden muss, um eine Anzeige der Daten im
           VEDA-IFrame zu ermoeglichen"""
        iframeurl = "http://entwicklung-etem.bg-kooperation.de/seminare/vedaseminare"
        vedaurl = "http://vedaentwicklung-etem.bg-kooperation.de"
        if vedaurl in url:
            url = url.replace(vedaurl, iframeurl)
            url = url.replace(';', '&DetailID=')
        return url
        
    def checkWebcode(self, suchtext, path):
        pcat = self.portal_catalog
        if path:
            brains = self.portal_catalog(Webcode=suchtext, path=path)
        else:
            brains = self.portal_catalog(Webcode=suchtext)
        url = ''
        if len(brains) == 1:
            url = brains[0].getURL()
            url = self.VedaIframe(url)
        elif len(brains) > 1 and path:
            url = '%s/@@search?Webcode=%s&path=%s' %(self.portal_url, suchtext, path)
        elif len(brains) > 1 and not path:
            url = '%s/@@search?Webcode=%s' %(self.portal_url, suchtext)
        return url

    def render(self):
        suchtext =  self.request.get("SearchableText", "")
        suchtext = suchtext.decode('utf-8')
        path =  self.request.get("path", "")
        if path:
           string.join(path[:-1], '/')
        if suchtext:
            webcodeurl = self.checkWebcode(suchtext, path)
            if webcodeurl:
                return self.request.response.redirect(webcodeurl)

        if ISolrConnectionConfig:
            config = queryUtility(ISolrConnectionConfig)
            facets = config.facets
            searchfacets = '&facet=true'
            for i in facets:
                searchfacets += '&facet.field=%s' %i
            parameter = {'SearchableText':suchtext.encode('utf-8')}
            params = urllib.urlencode(parameter)
            url = u'%s/@@search?%s%s' %(self.portal_url, params, searchfacets)
        else:
            parameter = {'SearchableText':suchtext.encode('utf-8')}
            params = urllib.urlencode(parameter)
            url = u'%s/@@search?%s' %(self.portal_url, params)
           
        if path:
            url = '%s&path=%s' %(url, path)
        return self.request.response.redirect(url)
