from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from bghw.seminare import seminareMessageFactory as _



class ISeminar(Interface):
    """Beschreibung der Eigenschaften des SSeminars"""

    # -*- schema definition goes here -*-
    text = schema.SourceText(
        title=_(u"Haupttext zum Seminar"),
        required=False,
        description=_(u"Bitte beschreiben Sie hier aausfuehrlich das angebotene Seminar."),
    )
#
    aform = schema.Object(
        title=_(u"Auswahl des Anmeldeformulars"),
        required=False,
        description=_(u"Bitte waehlen Sie hier aus, welches Anmeldeformular verwendet werden soll."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    prerequisites = schema.SourceText(
        title=_(u"Voraussetzungen fuer die Teilnahme"),
        required=False,
        description=_(u"Geben Sie hier die notwendigen Voraussetzungen fuer die Teilnahme an."),
    )
#
#    veranstalter = schema.TextLine(
#        title=_(u"Seminarveranstalter"),
#        required=True,
#        description=_(u"Bitte waehlen Sie aus, welche Sparte dieses Seminar anbietet."),
#    )
#
    contactName = schema.TextLine(
        title=_(u"Ansprechpartner"),
        required=True,
        description=_(u"Bitte tragen Sie hier den Ansprechpartner der BGHW ein."),
    )
#
    contactEmail = schema.TextLine(
        title=_(u"E-Mail"),
        required=True,
        description=_(u"Mailadresse des Ansprechpartners."),
    )
#
    contactPhone = schema.TextLine(
        title=_(u"Telefon"),
        required=True,
        description=_(u"Telefonnummer des Ansprechpartners."),
    )
#
    contactFax = schema.TextLine(
        title=_(u"Telefax"),
        required=False,
        description=_(u"Telefaxnummer des Ansprechpartners."),
    )
#
    referenz = schema.Object(
        title=_(u"Abschlusseiten"),
        required=False,
        description=_(u"Waehlen Sie hier geeignete Artikel, die nacheinander zum Abschluss der Anmeldung angezeigt werden."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    exturl = schema.TextLine(
        title=_(u"Externe URL"),
        required=False,
        description=_(u"Bitte geben Sie hier eine externe URL an, auf die fuer die Seminaranmeldung verwiesen werden soll"),
    )
#
    serviceid = schema.TextLine(
        title=_(u"Webservic-ID"),
        required=False,
        description=_(u"Bitte geben Sie hier die Parameter fuer den Aufruf des BGHW-Webservice an."),
    )
#
    datefile = schema.Bytes(
        title=_(u"Termindatei"),
        required=True,
        description=_(u"Hier koennen Sie eine Datei mit Seminarterminen hochladen."),
    )
#
