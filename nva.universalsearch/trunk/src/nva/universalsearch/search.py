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
            systems = set(config.systems)
            if 'system' in args:
                system = args['system']
                if isinstance(system, basestring):
                    system = [system]
                common = systems.intersection(system)
                if common:
                    systems = common
            args['system'] = list(systems)
        return super(UniversalSearch, self).buildQuery(default, **args)
