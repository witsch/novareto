# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

produktklasseVocab = SimpleVocabulary(
    [SimpleTerm(value=u'fein', title=u'fein'),
     SimpleTerm(value=u'mittel', title=u'mittel'),
     SimpleTerm(value=u'grob', title=u'grob')]
    )

ausgangsmaterialVocab = SimpleVocabulary(
    [SimpleTerm(value=u'Staerke', title=u'Stärke'),
     SimpleTerm(value=u'Calciumcarbonat', title=u'Calciumkarbonat'),
     SimpleTerm(value=u'Zucker', title=u'Zucker')]
    )

anwendungsgebieteVocab = SimpleVocabulary(
    [SimpleTerm(value=u'Farbreiniger', title=u'Farbreiniger'),
     SimpleTerm(value=u'Plattenreiniger', title=u'Plattenreiniger'),
     SimpleTerm(value=u'Feuchtwalzenreiniger', title=u'Feuchtwalzenreiniger'),
     SimpleTerm(value=u'Gummituchreiniger', title=u'Gummituchreiniger'),
     SimpleTerm(value=u'Reiniger_Leitstaende_Sensoren', title=u'Reiniger für Leitstände, Sensoren'),
     SimpleTerm(value=u'Klebstoffreiniger', title=u'Klebstoffreiniger'),]
    )
