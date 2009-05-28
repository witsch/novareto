from zope.interface import Interface

class IDocZeichenUtility(Interface):
    """Interface fuer Utility"""

class IDocZeichenView(Interface):
    """Interface fuer Utility"""

    def getVocabs():
	""" Return Vocabs"""

    def getVocabsEmpty():
	""" REturn Empty Vocabs """
