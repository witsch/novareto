from unittest import defaultTestLoader
from nva.universalsearch.tests.base import SolrTestCase

from transaction import abort, commit
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from collective.solr.interfaces import ISolrConnectionConfig
from collective.solr.interfaces import ISearch
from collective.solr.dispatcher import solrSearchResults
from collective.solr.utils import activate
from nva.universalsearch.interfaces import IUniversalSearchConfig


def indexForDifferentSystem(obj, system='Other'):
    from collective.solr.indexer import SolrIndexProcessor
    original = SolrIndexProcessor.getData

    def getData(self, obj, attributes=None):
        data, missing = original(self, obj, attributes)
        data['UID'] = system + '.' + data['UID']    # uid needs to be unique
        data['system'] = system
        return data, missing

    SolrIndexProcessor.getData = getData
    obj.processForm()
    commit()
    SolrIndexProcessor.getData = original


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
        indexForDifferentSystem(self.folder)
        system = self.portal.Title()
        self.assertEqual(len(self.search('+system:"%s"' % system)), 1)
        # without specifying the 'system' we should get two results
        self.assertEqual(len(self.search('+system:*')), 2)

    def testFullUriIsStoredInSolr(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        self.assertEqual([r.uri for r in self.search('*:*')],
            [self.folder.absolute_url()])

    def testFullCustomizedUriIsStoredInSolr(self):
        config = getUtility(IUniversalSearchConfig)
        config.site_url = 'http://foo.com'
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        self.assertEqual([r.uri for r in self.search('*:*')],
            ['http://foo.com/Members/' + self.folder.getId()])

    def testSystemsVocabulary(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        indexForDifferentSystem(self.folder)
        vocab = getUtility(IVocabularyFactory, name='nva.universalsearch.systems')
        self.assertEqual([i.token for i in vocab(self.portal)],
            ['Other', 'Plone site'])

    def testSearchResultsAreFilteredBySystems(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        indexForDifferentSystem(self.folder)
        # by default 'systems' isn't set and we're getting all results
        results = solrSearchResults(SearchableText='Foo')
        self.assertEqual(sorted([(r.Title, r.system) for r in results]),
            [('Foo', 'Other'), ('Foo', 'Plone site')])
        # after setting 'systems' we only get results for those...
        config = getUtility(IUniversalSearchConfig)
        config.systems = ['Plone site']
        results = solrSearchResults(SearchableText='Foo')
        self.assertEqual(sorted([(r.Title, r.system) for r in results]),
            [('Foo', 'Plone site')])

    def testSearchResultsCanBeLimitedViaRequestParameters(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        indexForDifferentSystem(self.folder)
        config = getUtility(IUniversalSearchConfig)
        config.systems = ['Plone site', 'Other']    # all 'systems' are allowed
        # explicitly setting an allowed 'system' limits results
        request = dict(SearchableText='[* TO *]', system='Other')
        results = solrSearchResults(request)
        self.assertEqual(sorted([(r.Title, r.system) for r in results]),
            [('Foo', 'Other')])

    def testOtherSystemsCannotBeSearchedViaRequestParameters(self):
        self.folder.processForm(values={'title': 'Foo'})
        commit()                        # indexing happens on commit
        indexForDifferentSystem(self.folder)
        config = getUtility(IUniversalSearchConfig)
        config.systems = ['Plone site']
        # explicitly setting another 'system' mustn't yield results
        request = dict(SearchableText='[* TO *]', system='Other')
        results = solrSearchResults(request)
        self.assertEqual(sorted([(r.Title, r.system) for r in results]),
            [('Foo', 'Plone site')])


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
