from unittest import defaultTestLoader
from nva.universalsearch.tests.base import SolrTestCase

from transaction import abort, commit
from zope.component import getUtility
from collective.solr.interfaces import ISolrConnectionConfig
from collective.solr.interfaces import ISearch
from collective.solr.utils import activate


class SolrServerTests(SolrTestCase):

    def afterSetUp(self):
        activate()
        self.portal.REQUEST.RESPONSE.write = lambda x: x    # ignore output
        self.maintenance = self.portal.unrestrictedTraverse('solr-maintenance')
        self.maintenance.clear()
        self.config = getUtility(ISolrConnectionConfig)
        self.search = getUtility(ISearch)

    def beforeTearDown(self):
        # due to the `commit()` in the tests below the activation of the
        # solr support in `afterSetUp` needs to be explicitly reversed,
        # but first all uncommitted changes made in the tests are aborted...
        abort()
        self.config.active = False
        commit()

    def testObjectCanBeSearchedViaSystemIndex(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        system = self.portal.Title()
        self.assertEqual(len(self.search('+system:"%s"' % system)), 1)

    def testFullUriIsStoredInSolr(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        self.assertEqual([r.uri for r in self.search('*:*')],
            [self.folder.absolute_url()])


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
