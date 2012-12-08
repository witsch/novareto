import Acquisition
from zope.component import getMultiAdapter, queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from nva.googlemaps.interfaces import IMyGoogleViewlet

from App.config import getConfiguration
config = getConfiguration()
configuration = config.product_config.get('googlemaps', dict())

googleurl = configuration.get('googleurl')
googlekey = configuration.get('googlekey', '')

class MyGoogleViewlet(ViewletBase):
    
    index =ViewPageTemplateFile("mygoogle.pt")

    def update(self):
        super(MyGoogleViewlet, self).update()
        if not IMyGoogleViewlet.providedBy(self.view):
            self.marker = False
            return
        self.marker = True
        self.googleurl = googleurl
        if googlekey:
            self.googleurl = "%s%s" % (googleurl, '&key='+googlekey)
        self.strnr = self.view.strnr
        self.plzort = self.view.plzort
        return
