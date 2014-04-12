from datetime import datetime
from DateTime import DateTime
from collective.solr import flare
from collective.solr.contentlisting import FlareContentListingObject

class PloneFlare(flare.PloneFlare):

    def getURL(self, relative=False):
        """ return the URI stored in Solr """
        return self.uri

class FlareContentListingObject(FlareContentListingObject):
   
    def pretty_title_or_id(self):
        return self.flare.pretty_title_or_id()


    def EffectiveDate(self, zone=None):
        date = self.flare.effective
        if date.year() < 1900:
            date = DateTime(datetime.now())
        return date
