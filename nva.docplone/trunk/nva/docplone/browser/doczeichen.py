from Products.Five import BrowserView
from nva.docplone.interfaces import IDocZeichenView
from zope.interface import implements
from zope.component import getUtility
from nva.docplone.interfaces import IDocZeichenUtility
from Products.Archetypes.public import DisplayList
from Products.Archetypes.utils import Vocabulary

null = DisplayList((
    ('', ''),
    ))

class DocZeichenView(BrowserView):
    implements(IDocZeichenView)

    def getVocabs(self):
	""" """
        dzu = getUtility(IDocZeichenUtility, name="nva.doczeichen.utility")
        dp = DisplayList(dzu.getHG())
        return Vocabulary(dp, self, 'docplone')

    def getVocabsEmpty(self):
	""" """
        return Vocabulary(null, self, 'docplone')
