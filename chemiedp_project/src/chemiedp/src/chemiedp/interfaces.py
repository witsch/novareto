# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from chemiedp.vocabularies import klasse, ausgangsmaterial
from chemiedp import MessageFactory as _
from chemiedp.vocabularies import anwendungsgebieteVocab


class IReinigungsmittel(Interface):
    """
    Description of the Example Type
    """

    anwendungsgebiete = schema.Set(title = _(u"Anwendungsgebiete"),
            description = _(u"Bitte wählen Sie die Anwendungsgebiete des Reinigungsmittels aus."),
            value_type = schema.Choice(title = _(u"Anwendungsgebiet"),
                                       vocabulary = anwendungsgebieteVocab),
            required = True,)

    flammpunkt = schema.Int(title = _(u"Flammpunkt"),
            description = _(u"Bitte geben Sie hier den Wert des Flammpunktes in Grad Celsius an."),
            required = False,)

    wertebereich = schema.Bool(title = _(u"Wertebereich für den Flammpunkt"),
            description = _(u"Bitte treffen Sie hier eine Auswahl wenn der Wertebereich für den\
                              Flammpunkt größer als der angegebene Zahlenwert ist."),
            required = False,)

    emissionsgeprueft = schema.Bool(title = _(u"Emissionsarmes Produkt"),
            description = _(u"Bitte markieren Sie hier, wenn für das Produkt die Kriterien des Gütesiegels\
                              erfüllt sind."),
            required = False,)


class IHersteller(Interface):
    """
    Hersteller von Produkten oder Maschinen
    """

    name = schema.TextLine(title = _(u"Name"),
            description = _(u"Bitte geben Sie hier den Namen des Herstellers ein."),
            required = True,)

    title = schema.TextLine(title = _(u"Titel"),
            description = _(u"Bitte geben Sie hier den Titel an der den Benutzern angezeigt werden soll."),
            required = True,)

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

    homepage = schema.URI(title = _("Hompage"),
            description = _(u"Bitte geben Sie hier die Internetadresse (http://www.example.de)\
                              des Herstellers ein."),
            required = False)

class IDruckbestaeubungspuder(Interface):
    """ 
    Description of the Example Type
    """

    name = schema.TextLine(title = _(u"Name"),
            description = _(u"Bitte geben Sie hier den Namen des Puders ein."),
            required = True,)

    title = schema.TextLine(title = _(u"Titel"),
            description = _(u"Bitte geben Sie hier den Titel an der den Benutzern angezeigt werden soll."),
            required = True,)

    produktklasse = schema.Choice(title = _(u"Produktklasse"),
            description = _(u"Bitte wählen Sie eine Produktklasse für das Druckbestäubungspuder aus."),
            vocabulary = klasse,
            required = True,)

    ausgangsmaterial = schema.Choice(title = _(u"Ausgangsmaterial"),
            description = _(u"Bitte wählen Sie das Ausgangsmaterial für das Druckbestäubungspuder aus."),
            vocabulary = ausgangsmaterial,
            required = True,)

    medianwert = schema.Float(title = _(u"Medianwert in µm"),
            description = _(u"Bitte geben Sie hier den Medianwert in Micrometer als Gleitkommawert an."),
            required = True,)

    volumenanteil = schema.Float(title = _(u"Volumenanteil < 10 µm"),
            description = _(u"Prozentuale Angabe des Volumenanteils der Partikel mit Korngrößen unterhalb\
                              10 µm am Gesamtvolumen der Puderprobe"),
            required = True,)

    maschinen = schema.TextLine(title = _(u"Maschinen"),
            description = _(u"Bitte geben Sie hier Maschinen an, bei denen dieses Druckbestäubungspuder\
                              explizit verwendet werden darf"),
            required = False,)
