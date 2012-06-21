from Products.Five import BrowserView
from zope.component import queryUtility
from collective.solr.interfaces import ISolrConnectionConfig


class SolrActiveView(BrowserView):

    def __call__(self):
        util = queryUtility(ISolrConnectionConfig)
        if util is not None:
            return util.active
        return False
