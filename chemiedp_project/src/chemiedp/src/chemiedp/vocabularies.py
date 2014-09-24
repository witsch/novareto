# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


from chemiedp import MessageFactory as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

anwendungsgebieteVocab = SimpleVocabulary(
    [SimpleTerm(value=u'Farbreiniger', title=_(u'Farbreiniger')),
     SimpleTerm(value=u'Plattenreiniger', title=_(u'Plattenreiniger')),
     SimpleTerm(value=u'Feuchtwalzenreiniger', title=_(u'Feuchtwalzenreiniger')),
     SimpleTerm(value=u'Gummituchregenerierer', title=_(u'Gummituchregenerierer')),
     SimpleTerm(value=u'Reiniger_Leitstaende_Sensoren', title=_(u'Reiniger für Leitstände, Sensoren')),
     SimpleTerm(value=u'Klebstoffreiniger', title=_(u'Klebstoffreiniger')),]
    )
