# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from chemiedp.vocabularies import produktklasseVocab, ausgangsmaterialVocab
from chemiedp import MessageFactory as _

class IHersteller(Interface):
    """ 
    Hersteller von Produkten oder Maschinen
    """

    name = schema.TextLine(title = _(u"Name"))

    title = schema.TextLine(title = _(u"Titel"))

    anschrift1 = schema.TextLine(title = _(u"Anschrift 1"),
            description = _(u"Bitte geben Sie hier die Anschrift des Herstellers ein."),
            required = True,)

    anschrift2 = schema.TextLine(title = _(u"Anschrift 2"),
            description = _(u"Bitte geben Sie hier einen evtl. Adresszusatz des Herstellers ein."),
            required = False,)

    anschrift3 = schema.TextLine(title = _(u"Anschrift 3"),
            description = _(u"Bitte geben Sie hier einen evtl. weiteren Adresszusatz des Herstellers ein."),
            required = False,)

    land = schema.TextLine(title = _("Land"),
            description = _(u"Bitte geben Sie hier das Land des Herstellers ein."),
            required = True,)

    telefon = schema.TextLine(title = _("Telefonnummer"),
            description = _(u"Bitte geben Sie hier die vollständige Telefonnummer mit Ländercode ein,\
                              Beispiel: +49 (0) 30 12345/678"),
            required = True,)

    telefax = schema.TextLine(title = _("Faxnummer"),
            description = _(u"Bitte geben Sie hier die vollständige Telefaxnummer mit Ländercode ein,\
                              Beispiel: +49 (0) 30 12345/777"),
            required = False,)

    email = schema.TextLine(title = _("E-Mail Adresse"),
            description = _(u"Bitte geben Sie hier die E-Mailadresse des Herstellers ein."),
            required = False,)

    homepage = schema.TextLine(title = _("Hompage"),
            description = _(u"Bitte geben Sie hier die Internetadresse (http://www.example.de)\
                              des Herstellers ein."),
            required = False)


class IDruckbestaeubungspuder(Interface):
    """ 
    Description of the Example Type
    """

    produktklasse = schema.Choice(title = _(u"Produktklasse"),
            description = _(u"Bitte wählen Sie eine Produktklasse für das Druckbestäubungspuder aus."),
            vocabulary = produktklasseVocab,
            required = True,)

    ausgangsmaterial = schema.Choice(title = _(u"Ausgangsmaterial"),
            description = _(u"Bitte wählen Sie das Ausgangsmaterial für das Druckbestäubungspuder aus."),
            vocabulary = ausgangsmaterialVocab,
            required = True,)

    medianwert = schema.Float(title = _(u"Medianwert in µm"),
            description = _(u"Bitte geben Sie hier den Medianwert in Micrometer als Gleitkommawert an."),
            required = True,)

    volumenanteil = schema.Float(title = _(u"Volumenanteil < 10 µm"),
            description = _(u"Prozentuale Angabe des Volumenanteils der Partikel mit Korngrößen unterhalb\
                              10 µm am Gesamtvolumen der Puderprobe"),
            required = True,)

    maschinen = schema.List(title = _(u"Maschinen mit Ausschlußkriterien"),
            description = _(u"Bitte geben Sie hier Maschinen an, bei denen dieses Druckbestäubungspuder\
                              explizit nicht verwendet werden darf (ein Eintrag pro Zeile)"),
            value_type = schema.TextLine(title = _(u"Druckbestäubungspuder")),
            required = False,)

