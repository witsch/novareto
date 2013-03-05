# -*- coding: utf-8 -*-
from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema
from nva.bsbetreuung import bsbetreuungMessageFactory as _

class IFragestellung(Interface):
    """Fragestellung zu einer Aufgabe der betriebsspezifischen Betreuung"""

    # -*- schema definition goes here -*-
    fieldtype = schema.Text(
        title=_(u"Feldtyp"),
        required=True,
        description=_(u"Bitte waehlen Sie hier die Art des Feldes aus."),
    )
#
    hilfe = schema.SourceText(
        title=_(u"Hilfetext"),
        required=False,
        description=_(u"Bitte beschreiben Sie hier eine Hilfe fuer diese Fragestellung."),
    )
#
    faktor = schema.Float(
        title=_(u"Faktor"),
        required=True,
        description=_(u"Bitte tragen Sie hier einen Faktor fuer die Berechnung des Betreuungsaufwandes ein. Sind keine Antwortoptionen angegeben, gilt dieser Faktor fuer diese Fragestellung; die Frage wird dann nicht eingeblendet. Sind dagegen Antwortoptionen angegeben, kann dieser Faktor als zusaetzlicher Gewichtungsfaktor genutzt werden."),
    )
#
    optionen = schema.List(
        title=_(u"Optionen"),
        required=False,
        description=_(u"Bitte beschreiben Sie hier die Optionen fuer dieses Feld. Es gilt folgende Syntax: value|text. Beispiel: 1.0|mehr als 50% der Beschaeftigten."),
    )
#
    
