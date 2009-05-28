from zope.component import getUtility
from nva.docplone.interfaces import IDocZeichenUtility
from Products.Archetypes.public import LinesField, DisplayList
from Products.Archetypes.utils import Vocabulary 
from archetypes.schemaextender.field import ExtensionField

null = DisplayList((
    ('', ''),
    ))


class DocPloneField(ExtensionField, LinesField):
    """A trivial field."""

    def getVocabs(self, vocab):
        dzu = getUtility(IDocZeichenUtility, name="nva.doczeichen.utility")
        dp = DisplayList(dzu.getHG())
	return Vocabulary(dp, self, 'docplone')

    def getVocabsEmpty(self):
	return Vocabulary(null, self, 'docplone')

    def getVocabsAZ(self):
        dzu = getUtility(IDocZeichenUtility, name="nva.doczeichen.utility")
        dp = DisplayList(dzu.getAnhangzahlen())
	return Vocabulary(dp, self, 'docplone')

    def getVocabsAB(self):
        dzu = getUtility(IDocZeichenUtility, name="nva.doczeichen.utility")
        dp = DisplayList(dzu.getAnhangbegriffe())
	return Vocabulary(dp, self, 'docplone')
