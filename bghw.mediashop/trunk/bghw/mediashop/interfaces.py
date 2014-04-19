# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary

class IArtikelListe(Interface):
    """Schema fuer die Artikelliste einer Bestellung"""

    artikel = schema.TextLine(title = u'Artikelnummer', required = True)

    beschreibung = schema.TextLine(title = u'Beschreibung', required = True)

    anzahl = schema.Int(title = u'Bestellmenge', required = True)


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
                                      required = True,)

    firma = schema.TextLine(title = u'Firma', required = True)

    anrede = schema.Choice(title = u'Anrede',
                           description = u'Bitte treffen Sie eine Auswahl.',
                           vocabulary = SimpleVocabulary.fromValues([u'Auswahl', u'Herr', u'Frau']),
                           required = True,)

    titel = schema.Choice(title = u'Titel',
                          description = u'Bitte treffen Sie eine Auswahl.',
                          vocabulary = SimpleVocabulary.fromValues([u'kein Titel', u'Dr.', u'Prof.']),
                          default = u'kein Titel',
                          required = False,)

    vorname = schema.TextLine(title = u'Vorname', required = True)

    name = schema.TextLine(title = u'Name', required = True)

    strhnr = schema.TextLine(title = u'Straße und Hausnummer', required = True)

    plz = schema.TextLine(title = u'Postleitzahl', required = True)

    ort = schema.TextLine(title = u'Ort', required = True)

    telefon = schema.TextLine(title = u'Telefon', required = False)

    email = schema.TextLine(title = u'eMail', required = True)

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

    hinweis = schema.Bool(title = u'Hinweise zur Bestellung',
                          description = u'Einverständniserklärung mit den Nutzungsbedingungen der BGHW\
                          die der Benutzer bestätigen muss.',
                          default = False,
                          required = True)


