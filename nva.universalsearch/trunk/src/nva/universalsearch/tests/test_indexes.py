from unittest import defaultTestLoader
from nva.universalsearch.tests.base import SolrTestCase

from transaction import abort, commit
from zope.component import getUtility
from collective.solr.interfaces import ISolrConnectionConfig
from collective.solr.interfaces import ISolrConnectionManager
from collective.solr.utils import activate
from collective.solr.tests.utils import numFound


class SolrServerTests(SolrTestCase):

    def afterSetUp(self):
        activate()
        self.portal.REQUEST.RESPONSE.write = lambda x: x    # ignore output
        self.maintenance = self.portal.unrestrictedTraverse('solr-maintenance')
        self.maintenance.clear()
        self.config = getUtility(ISolrConnectionConfig)

    def beforeTearDown(self):
        # due to the `commit()` in the tests below the activation of the
        # solr support in `afterSetUp` needs to be explicitly reversed,
        # but first all uncommitted changes made in the tests are aborted...
        abort()
        self.config.active = False
        commit()

    def testObjectCanBeSearchedViaSystemIndex(self):
        self.folder.processForm(values={'title': 'Foo'})
        connection = getUtility(ISolrConnectionManager).getConnection()
        commit()                        # indexing happens on commit
        system = self.portal.Title()
        result = connection.search(q='+system:"%s"' % system).read()
        self.assertEqual(numFound(result), 1)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
