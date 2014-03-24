from zope.interface import implements
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.solr.interfaces import ISearch
from collective.solr.search import Search
from nva.universalsearch.interfaces import IUniversalSearchConfig


class UniversalSearch(Search):
    implements(ISearch)

    def buildQuery(self, default=None, system=None, **args):
        """ extend default by adding query param for 'systems' """
        config = getUtility(IUniversalSearchConfig)
        if config.systems:
            systems = set(config.systems)
            if system is not None:
                if isinstance(system, basestring):
                    system = [system]
                common = systems.intersection(system)
                if common:
                    systems = common
            system = list(systems)
        if 'path_parents' in args and not 'path_depth' in args:
            portal = getUtility(IPloneSiteRoot)
            portal_path = '/'.join(portal.getPhysicalPath())
            if args['path_parents'] == '"\\%s"' % portal_path:
                del args['path_parents']
        return super(UniversalSearch, self).buildQuery(default, system=system, **args)
