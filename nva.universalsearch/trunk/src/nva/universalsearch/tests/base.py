from Products.PloneTestCase import PloneTestCase as ptc
from Testing.ZopeTestCase import Sandboxed
from nva.universalsearch.tests.layer import layer


ptc.setupPloneSite()


class SolrTestCase(Sandboxed, ptc.PloneTestCase):
    """ base class for integration tests """

    layer = layer
