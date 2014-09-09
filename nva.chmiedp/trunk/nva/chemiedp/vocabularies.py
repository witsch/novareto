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

anwendungsgebieteVocab = SimpleVocabulary(
    [SimpleTerm(value=u'Farbreiniger', title=_(u'Farbreiniger')),
     SimpleTerm(value=u'Plattenreiniger', title=_(u'Plattenreiniger')),
     SimpleTerm(value=u'Feuchtwalzenreiniger', title=_(u'Feuchtwalzenreiniger')),
     SimpleTerm(value=u'Gummituchreiniger', title=_(u'Gummituchreiniger')),
     SimpleTerm(value=u'Reiniger_Leitstaende_Sensoren', title=_(u'Reiniger für Leitstände, Sensoren')),
     SimpleTerm(value=u'Klebstoffreiniger', title=_(u'Klebstoffreiniger')),]
    )

einstufungVocab = SimpleVocabulary(
    [SimpleTerm(value=u'xi-reizend', title=_(u'Xi; Reizend')),
     SimpleTerm(value=u'xn-gesundheitsschaedlich', title=_(u'Xn; gesundheitsschädlich')),
     SimpleTerm(value=u'signalwort-achtung', title=_(u'Signalwort: Achtung')),
     SimpleTerm(value=u'signalwort-gefahr', title=_(u'Signalwort: Gefahr')),
     SimpleTerm(value=u'piktogramm-achtung', title=_(u'Piktogramm: Achtung')),
     SimpleTerm(value=u'piktogramm-aetzend', title=_(u'Piktogramm: Ätzend')),
     SimpleTerm(value=u'piktogramm-entflammbar', title=_('Piktogramm: Entflammbar')),]
    )

zweckVocab = SimpleVocabulary(
    [SimpleTerm(value=u'buchdruck', title=_(u'Buchdruck')),
     SimpleTerm(value=u'flexodruck', title=_(u'Flexodruck')),
     SimpleTerm(value=u'siebdruck', title=_(u'Siebdruck')),
     SimpleTerm(vaule=u'farbreiniger_alle_druckverfahren', title=_(u'Farbreiniger alle Druckverfahren')),
     SimpleTerm(value=u'offsetdruck', title=_(u'Offsetdruck')),
     SimpleTerm(value=u'waschanlage', title=_(u'Waschanlage')),
     SimpleTerm(value=u'tiefdruck', title=_(u'Tiefdruck')),
     SimpleTerm(value=u'klischeereiniger', title=_(u'Klischeereiniger')),]
     )
