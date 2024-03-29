# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema import ValidationError
from uvc.validation import validateMail, validatePhone, validatePLZ
from bghw.mediashop.mnrtest import mnrtest

class NotValidMnr(ValidationError):
    u""" Für die Bestellung im Medienshop der BGHW ist eine gültige Mitgliedsnummer erforderlich. Sollte Ihnen die 
         Mitgliedsnummer nicht vorliegen oder Ihr Betrieb kein Mitglied der BGHW sein, wenden Sie sich bitte per E-Mail
         an: medien@bghw.de. """

def validateMNR(value):
    if value:
        if len(value) == 10:
            value = value.replace('-', '')
        if len(value) != 9 or not value.isdigit():
            raise NotValidMnr(value)
        if not  mnrtest(value):
            raise NotValidMnr(value)
    return True

class NotValidAnrede(ValidationError):
    u""" Bitte treffen Sie eine Auswahl 'Herr' oder 'Frau' für die Anrede. """

def validateAnrede(value):
    if value:
        if value == u'Auswahl':
            raise NotValidAnrede(value)
    return True

class NotValidHinweis(ValidationError):
    u""" Bitte bestätigen Sie die Nutzungsbedingungen für den BGHW-Medienshop. """


def validateHinweis(value):
    if value:
        if value == u'nein':
            raise NotValidHinweis(value)
    return True

class IArtikelListe(Interface):
    """Schema fuer die Artikelliste einer Bestellung"""

    artikel = schema.TextLine(title = u'Art.-nr.', required = True)

    bestellnummer = schema.TextLine(title = u'Bestellnummer', required = True)

    beschreibung = schema.TextLine(title = u'Beschreibung', required = True)

    anzahl = schema.Int(title = u'Anzahl', required = True)


class IBestellung(Interface):
    """Schema fuer das Bestellformular"""

    bestellung = schema.List(title = u'Ihre Bestellung bei der BGHW',
                             description = u'Bitte kontrollieren Sie Ihre Auswahl und korrigieren\
                             eventuell die angegebenen Bestellmengen',
                             value_type = schema.Object(title = u'Bestellung',
                                                        schema = IArtikelListe),
                             required = True,)

    mitgliedsbetrieb = schema.Bool(title = u'Mitgliedsbetrieb der BGHW',
                                   description = u'Bitte bestätigen Sie hier die Mitgliedschaft Ihres\
                                   Betriebes bei der BGHW. Bitte beachten Sie, dass nur Mitgliedsbetriebe\
                                   der BGHW die Artikel des Medienshops auf diesem Weg bestellen können.',
                                   default = True,)

    mitgliedsnummer = schema.TextLine(title = u'Mitgliedsnummer',
                                      description = u'Die Artikel des Medienshops können nur von\
                                      Mitgliedsbetrieben der BGHW auf diesem Weg bestellt werden.\
                                      Bitte geben Sie hier Ihre Mitgliedsnummer bei der BGHW an.',
                                      required = True,
                                      constraint = validateMNR,)

    firma = schema.TextLine(title = u'Firma', required = True)

    anrede = schema.Choice(title = u'Anrede',
                           description = u'Bitte treffen Sie eine Auswahl.',
                           vocabulary = SimpleVocabulary.fromValues([u'Auswahl', u'Herr', u'Frau']),
                           required = True,
                           constraint = validateAnrede,)

    titel = schema.Choice(title = u'Titel',
                          description = u'Bitte treffen Sie eine Auswahl.',
                          vocabulary = SimpleVocabulary.fromValues([u'kein Titel', u'Dr.', u'Prof.']),
                          default = u'kein Titel',
                          required = False,)

    vorname = schema.TextLine(title = u'Vorname', required = True)

    name = schema.TextLine(title = u'Name', required = True)

    strhnr = schema.TextLine(title = u'Straße und Hausnummer', required = True)

    plz = schema.TextLine(title = u'Postleitzahl', required = True, constraint=validatePLZ)

    ort = schema.TextLine(title = u'Ort', required = True)

    telefon = schema.TextLine(title = u'Telefon', required = False)

    email = schema.TextLine(title = u'E-Mail', required = True, constraint=validateMail)

    lieferung = schema.Bool(title = u'abweichende Lieferadresse',
                            description = u'Bitte hier markieren, wenn eine abweichende Lieferanschrift\
                            gewünscht wird.',
                            default = False,)

    a_firma = schema.TextLine(title = u'Firma', required = False)

    a_anrede = schema.Choice(title = u'Anrede',
                             description = u'Bitte treffen Sie eine Auswahl.',
                             vocabulary = SimpleVocabulary.fromValues([u'Auswahl', u'Herr', u'Frau']),
                             required = False,)

    a_titel = schema.Choice(title = u'Titel',
                            description = u'Bitte treffen Sie eine Auswahl.',
                            vocabulary = SimpleVocabulary.fromValues([u'kein Titel', u'Dr.', u'Prof.']),
                            default = u'kein Titel',
                            required = False,)

    a_vorname = schema.TextLine(title = u'Vorname', required = False)

    a_name = schema.TextLine(title = u'Name', required = False)

    a_strhnr = schema.TextLine(title = u'Straße und Hausnummer', required = False)

    a_plz = schema.TextLine(title = u'Postleitzahl', required = False)

    a_ort = schema.TextLine(title = u'Ort', required = False)

    hinweis = schema.Choice(title = u'Hinweise zur Bestellung',
                          description = u'Einverständniserklärung mit den Nutzungsbedingungen der BGHW\
                          die der Benutzer bestätigen muss.',
                          vocabulary = SimpleVocabulary.fromValues([u'ja', u'nein']),
                          required = True,
                          constraint = validateHinweis,)


