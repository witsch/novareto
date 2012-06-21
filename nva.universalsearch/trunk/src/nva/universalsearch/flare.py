from collective.solr import flare


class PloneFlare(flare.PloneFlare):

    def getURL(self, relative=False):
        """ return the URI stored in Solr """
        return self.uri
