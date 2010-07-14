from logging import getLogger
from zope.interface import implements
from zope.component import queryUtility
from collective.solr.search import Search, quote
from nva.universalsearch.config import MULTIPLESITES, FACETEDFIELDS, ROOTS

from collective.solr.interfaces import ISearch

from collective.solr.interfaces import ISolrConnectionConfig
from collective.solr.interfaces import ISolrConnectionManager
from collective.solr.interfaces import ISearch
from collective.solr.parser import SolrResponse
from collective.solr.exceptions import SolrInactiveException


logger = getLogger('nva.universal.search')


class UniversalSearch(Search):
    implements(ISearch)


    def searchii(self, query, **parameters):
        """ perform a search with the given querystring and parameters """
        manager = self.getManager()
        manager.setSearchTimeout()
        connection = manager.getConnection()
        if connection is None:
            raise SolrInactiveException
        if not 'rows' in parameters:
            config = queryUtility(ISolrConnectionConfig)
            parameters['rows'] = config.max_results or ''
        if isinstance(query, dict):
            query = ' '.join(query.values())
        if FACETEDFIELDS:
            parameters['facet'] = "on"
            parameters['facet_limit'] = '-1'
            parameters['facet.field'] = FACETEDFIELDS
        logger.debug('searching for %r (%r)', query, parameters)
        response = connection.search(q=query, **parameters)
	results = SolrResponse(response)
        response.close()
        manager.setTimeout(None)
        return results

    #__call__ = search

    def buildQuery(self, default=None, **args):
        """ helper to build a querystring for simple use-cases """
        logger.debug('building query for "%r", %r', default, args)
        schema = self.getManager().getSchema() or {}
        defaultSearchField = getattr(schema, 'defaultSearchField', None)
        args[None] = default
        query = {}

	if MULTIPLESITES:
            if args.get('parentPaths','') in ROOTS:
	        del args['parentPaths']
        for name, value in args.items():
            field = schema.get(name or defaultSearchField, None)
            if field is None or not field.indexed:
                logger.debug('dropping unknown search attribute "%s" (%r)',
                    name, value)
                continue
            if isinstance(value, bool):
                value = str(value).lower()
            elif not value:     # solr doesn't like empty fields (+foo:"")
                continue
            elif isinstance(value, (tuple, list)):
                #quoted = False
                #value = '(%s)' % ' '.join(map(quote, value))
                def quoteitem(term):
                    if isinstance(term, unicode):
                        term = term.encode('utf-8')
                    quoted = quote(term)
                    if not quoted.startswith('"') and not quoted == term:
                        quoted = quote('"' + term + '"')
                    return quoted
                value = '(%s)' % ' '.join(map(quoteitem, value))
            elif isinstance(value, basestring):
                value = quote(value)
                if not value:       # don't search for an empty string, even if quoted
                    continue
            else:
                logger.info('skipping unsupported value "%r" (%s)',
                    value, name)
                continue
            if name is None:
                if value and value[0] not in '+-':
                    value = '+%s' % value
            else:
                value = '+%s:%s' % (name, value)
            query[name] = value
        logger.debug('built query "%s"', query)

        return query

