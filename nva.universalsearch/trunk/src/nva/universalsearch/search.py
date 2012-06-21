from zope.interface import implements
from zope.component import getUtility
from collective.solr.interfaces import ISearch
from collective.solr.search import Search
from nva.universalsearch.interfaces import IUniversalSearchConfig


class UniversalSearch(Search):
    implements(ISearch)

    def buildQuery(self, default=None, **args):
        """ extend default by adding query param for 'systems' """
        config = getUtility(IUniversalSearchConfig)
        if config.systems:
            args['system'] = config.systems
        return super(UniversalSearch, self).buildQuery(default, **args)
