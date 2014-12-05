# -*- coding: utf-8 -*-

def createMessage(data, bestellnummer=None):
    message = u"""\
Sehr geehrte Dame, sehr geehrter Herr,

Ihre Bestellung im Medienshop ist unter folgender Bestell-ID bei uns eingegangen:

"""


    if bestellnummer:
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
