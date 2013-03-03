from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema
from nva.bsbetreuung import bsbetreuungMessageFactory as _

class IAufgabe(Interface):
    """Aufgabe in der betriebbspezifischen Betreuung"""

    # -*- schema definition goes here -*-
    startend = schema.Object(
        title=_(u"Weiterleitung"),
        required=False,
        description=_(u"Auf der ersten Seite des Wizards bitte hier auf die Einleitung referenzieren, auf der letzten Seite des Wizards auf die Seite mit der Ergebnisuebersicht"),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    nummer = schema.TextLine(
        title=_(u"Nummer des Aufgabenfeldes"),
        required=True,
        description=_(u"Unter dieser Nummer werden die Benutzereingaben fuer dieses Aufgabenfeld gespeichert."),
    )
#
    aufgabentext = schema.SourceText(
        title=_(u"Aufgabentext"),
        required=True,
        description=_(u"Bitte beschreiben Sie hier die Aufgabe."),
    )
#
    hilfe = schema.SourceText(
        title=_(u"Hilfetext"),
        required=False,
        description=_(u"Bitte machen Sie hier eine Eingabe, wenn Sie zusaetzliche Hilfestellung fuer ddieses Aufgabengebiet anbieten wollen."),
    )
#
    basiszeitfaktor = schema.Float(
        title=_(u"Basiszeitfaktor"),
        required=True,
        description=_(u"Bitte geben Sie in Stunden/Jahr an, welcher Basiszeitfaktor fuer dieses Aufgabenfeld gelten soll."),
    )
#
    minimum = schema.Float(
        title=_(u"Minimum Stunden/Jahr"),
        required=False,
        description=_(u"Bitte geben Sie hier an, welcher minimale Aufwand in Stunden/Jahr fuer dieses Aufgabenfeld gelten soll."),
    )
#
    maximum = schema.Float(
        title=_(u"Maximum Stunden/Jahr"),
        required=False,
        description=_(u"Bitte geben Sie hier den Maximalwert in Stunden/Jahr fuer dieses Aufgabenfeld  ein."),
    )
#
    alternativtext = schema.TextLine(
        title=_(u"Kommentar"),
        required=False,
        description=_(u"Der Kommentar wird eingeblendet, wenn Sie keine Fragestellungen zu diesem Feld ausgewaehlt haben."),
    )
#
    fragen = schema.Object(
        title=_(u"Fragestellungen"),
        required=False,
        description=_(u"Bitte waehlen Sie aus, welche Fragestellungen Ihrer Aufgabe zugeordnet werdenn  sollen."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    
