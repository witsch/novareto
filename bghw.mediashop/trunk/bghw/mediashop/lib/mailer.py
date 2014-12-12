# -*- coding: utf-8 -*-
from datetime import datetime
from time import strftime

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

def createOrderMessage(data, bestellnummer=None):
    """EMail mit der Bestellung an die Medienverwaltung"""
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

Mitgliedsnummer: %s
Firma: %s
Titel: %s
Anrede: %s
Vorname: %s
Name: %s
""" % (data.get('mitgliedsnummer'), 		
       data.get('firma'), 		
       data.get('titel'), 		
       data.get('anrede'), 		
       data.get('vorname'), 		
       data.get('name'),)

    return message 
