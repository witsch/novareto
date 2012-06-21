from Testing.ZopeTestCase import installPackage
from Zope2.App import zcml

from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer


class SolrLayer(BasePTCLayer):
    """ layer for solr integration tests """

    def afterSetUp(self):
        from collective import indexing, solr
        zcml.load_config('configure.zcml', indexing)
        zcml.load_config('configure.zcml', solr)
        installPackage('collective.indexing', quiet=True)
        installPackage('collective.solr', quiet=True)
        installPackage('nva.universalsearch', quiet=True)
        self.addProfile('nva.universalsearch:default')

layer = solr = SolrLayer(bases=[ptc_layer])
