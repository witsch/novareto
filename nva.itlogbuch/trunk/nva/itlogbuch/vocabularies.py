# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from nva.itlogbuch import itlogbuchMessageFactory as _

def systemvocab(context=None):
    """Dieses Vocabulary dient zur Auswahl der Systemkategorie"""
    vocab = SimpleVocabulary([
            SimpleTerm(value='Produktion', title=_(u'Produktion')),
            SimpleTerm(value='Shadow', title=_(u'Shadow')),
            SimpleTerm(value='Entwicklung', title=_(u'Entwicklung')),
            SimpleTerm(value='Training', title=_(u'Training')),
            ])
    return vocab

def aenderungvocab(context=None):
    """Dieses Vocabulary dient zur Auswahl der Aenderungskategorie"""
    vocab = SimpleVocabulary([
            SimpleTerm(value='adabas_prod', title=_(u'Adabas')),
            SimpleTerm(value='uv dms', title=_(u'UV DMS')),
            SimpleTerm(value='extranet', title=_(u'Extranet')),
            SimpleTerm(value='formdesigner', title=_(u'Formdesigner')),
            SimpleTerm(value='host', title=_(u'Host')),
            SimpleTerm(value='hvv', title=_(u'HVV')),
            SimpleTerm(value='intranet', title=_(u'Intranet')),
            SimpleTerm(value='java', title=_(u'Java')),
            SimpleTerm(value='linux', title=_(u'Linux')),
            SimpleTerm(value='natural', title=_(u'Natural')),
            SimpleTerm(value='netzwerk', title=_(u'Netzwerk')),
            SimpleTerm(value='pc-programme', title=_(u'PC-Programme')),
            SimpleTerm(value='shared services', title=_(u'Shared Services')),
            SimpleTerm(value='sonstige', title=_(u'Sonstige')),
            SimpleTerm(value='sun', title=_(u'Sun')),
            ])
    return vocab

