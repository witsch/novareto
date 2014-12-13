# -*- coding: utf-8 -*-
from datetime import datetime
from time import strftime
from zeam.form.base.markers import NO_VALUE

def createMessage(data, bestellnummer=None):
    message = u"""\
Sehr geehrte Dame, sehr geehrter Herr,

Ihre Bestellung im Medienshop ist unter folgender Bestell-ID bei uns eingegangen:

"""
    if not bestellnummer:
        bestellnummer = datetime.now().strftime('%d%m%Y%H%M') + data.get('mitgliedsnummer')[-5:]

    message += u"""\
Bestell-ID %s

""" %bestellnummer

    message += u"""\
Sie haben folgende Artikel bei uns bestellt:

"""

    for i in data.get('bestellung'):
        message += u"""\
  -  Bestell-Nummer %s (Artikelnummer %s) %s, Bestellmenge:%s

""" % (i.bestellnummer, i.artikel, i.beschreibung, i.anzahl)

    else:
        message += u"""\
Bei Rückfragen wenden Sie sich bitte unter Angaben Ihre Bestell-ID per Email an medien@bghw.de.

"""
        
    message += u"""\
Mit freundlichen Grüßen

Ihre Berufsgenossenschaft Handel und Warenlogistik."""

    return message

def formatData(data):
    if data == NO_VALUE:
        return ''
    return data


def createOrderMessage(data, bestellnummer=None):
    """EMail mit der Bestellung an die Medienverwaltung"""
   
    mytitel = data.get('titel')
    if mytitel == u'kein Titel':
        mytitel = ''

    a_titel = data.get('a_titel')
    if a_titel == u'kein Titel':
        a_titel = ''

    message = u"""\
Das ist die Bestellung des Mitgliedsbetriebes:
"""
    if not bestellnummer:
        bestellnummer = datetime.now().strftime('%d%m%Y%H%M') + data.get('mitgliedsnummer')[-5:]

    message += u"""\
Bestell-ID %s

""" %bestellnummer

    for i in data.get('bestellung'):
        message += """\

Artikelnummer: %s
Bezeichnung: %s
Menge: %s
""" % (i.artikel, i.beschreibung, i.anzahl)

    message += """\

Kontaktdaten:

Mitgliedsnummer: %s
E-Mail: %s
Telefon: %s
""" % (data.get('mitgliedsnummer'), 		
       data.get('email'),
       formatData(data.get('telefon')))

    message += """\

Adressdaten:

%s
%s %s %s %s
%s
%s %s
""" % (data.get('firma'),
       data.get('anrede'),
       mytitel,
       data.get('vorname'),
       data.get('name'),
       data.get('strhnr'),
       data.get('plz'),
       data.get('ort'))

    if data.get('lieferung'):
        message += """\

Abweichende Lieferadresse:

%s
%s %s %s %s
%s
%s %s
""" % (formatData(data.get('a_firma')),
       formatData(data.get('a_anrede')),
       a_titel,
       formatData(data.get('a_vorname')),
       formatData(data.get('a_name')),
       formatData(data.get('a_strhnr')),
       formatData(data.get('a_plz')),
       formatData(data.get('a_ort')))
    
    return message 
