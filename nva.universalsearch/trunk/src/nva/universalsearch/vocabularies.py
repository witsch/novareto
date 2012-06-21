from zope.component import queryUtility, getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from collective.solr.interfaces import ISolrConnectionManager
from collective.solr.interfaces import ISearch
from nva.universalsearch.interfaces import IUniversalSearchConfig


class Systems(object):
    """ vocabulary provider yielding all values for the 'system' index """
    implements(IVocabularyFactory)

    def __call__(self, context):
        config = getUtility(IUniversalSearchConfig)
        items = set(config.systems)
        manager = queryUtility(ISolrConnectionManager)
        if manager is not None and manager.getSchema() is not None:
            search = queryUtility(ISearch)
            params = {'rows': 0, 'facet': 'true', 'facet.field': 'system'}
            result = search('+system:*', **params)
            items.update(result.facet_counts['facet_fields']['system'])
        return SimpleVocabulary([SimpleTerm(item) for item in sorted(items)])
