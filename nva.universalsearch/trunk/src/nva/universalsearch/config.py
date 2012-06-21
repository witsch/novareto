from persistent import Persistent
from zope.interface import implements
from nva.universalsearch.interfaces import IUniversalSearchConfig


SYSTEM = "intranet"
MULTIPLESITES = True
FACETEDFIELDS = ["system", "portal_type", "review_state"]
ROOTS = ["/bghwintranet",] 


class UniversalSearchConfig(Persistent):
    implements(IUniversalSearchConfig)

    def __init__(self):
        self.systems = []

    def getId(self):
        """ return a unique id to be used with GenericSetup """
        return 'universalsearch'
