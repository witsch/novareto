from persistent import Persistent
from zope.interface import implements
from nva.universalsearch.interfaces import IUniversalSearchConfig


class UniversalSearchConfig(Persistent):
    implements(IUniversalSearchConfig)

    def __init__(self):
        self.site_url = None
        self.systems = []

    def getId(self):
        """ return a unique id to be used with GenericSetup """
        return 'universalsearch'
