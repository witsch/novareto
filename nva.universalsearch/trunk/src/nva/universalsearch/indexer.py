from zope.interface import implements
from logging import getLogger
from collective.solr.indexer import (SolrIndexProcessor,
     indexable)
from nva.universalsearch.interfaces import IUniversalSearchQueueProcessor
from collective.solr.utils import prepareData

from collective.solr.solr import SolrException
from zope.component import getMultiAdapter


logger = getLogger('nva.universalsearch.indexer')


class UniversalSearchQueueProcessor(SolrIndexProcessor):
    implements(IUniversalSearchQueueProcessor)

    def index(self, obj, attributes=None):
        conn = self.getConnection()
        if conn is not None and indexable(obj):
            data, missing = self.getData(obj, attributes)
            ### Hook um die Variable system zu setzen
            system = getMultiAdapter((obj, obj.REQUEST), name="plone_portal_state")
            data['system'] = system.portal_title()
            logger.info('system --> %s', data['system'])
            data['uri'] = obj.absolute_url()
            prepareData(data)
            schema = self.manager.getSchema()
            if schema is None:
                logger.warning('unable to fetch schema, skipping indexing of %r', obj)
                return
            uniqueKey = schema.get('uniqueKey', None)
            if uniqueKey is None:
                logger.warning('schema is missing unique key, skipping indexing of %r', obj)
                return
            if data.get(uniqueKey, None) is not None and not missing:
                try:
                    logger.debug('indexing %r (%r)', obj, data)
                    conn.add(**data)
                    #import transaction; transaction.commit()
                    #print '###'*10
                except (SolrException, error):
                    logger.exception('exception during indexing %r', obj)

            else:
                print "kein Key, %s " %obj.id
