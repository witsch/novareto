# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from nva.chemiedp import MessageFactory as _

klasse = SimpleVocabulary(
    [SimpleTerm(value=u'fein', title=_(u'fein')),
     SimpleTerm(value=u'mittel', title=_(u'mittel')),
     SimpleTerm(value=u'grob', title=_(u'grob'))]
    )

ausgangsmaterial = SimpleVocabulary(
    [SimpleTerm(value=u'Staerke', title=_(u'Stärke')),
     SimpleTerm(value=u'Calciumcarbonat', title=_(u'Calciumkarbonat')),
     SimpleTerm(value=u'Zucker', title=_(u'Zucker'))]
    )
