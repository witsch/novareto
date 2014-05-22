# -*- coding: utf-8 -*-

def createMessage(data, bestellnummer=None):
    message = u"""\
Sehr geehrte Dame, sehr geehrter Herr,

Ihre Bestellung im Medienshop der BGHW ist bei uns eingegangen. Sie haben folgende
Artikel bei uns bestellt:"""

    for i in data.get('bestellung'):
        message += u"""%s %s Bestellmenge: %s""" % (i.artikel, i.beschreibung, i.anzahl)


    if bestellnummer:
        message += u"""\
Bei Rückfragen wenden Sie sich bitte per E-Mail an: medien@bghw.de und geben dabei bitte 
stets Ihre Bestellnummer an: %s.""" %bestellnummer

    else:
        message += u"""\
Bei Rückfragen wenden Sie sich bitte per E-Mail an: medien@bghw.de und geben dabei folgende
Nummer an: EMail*****%s.""" %data.get('mitgliedsnummer')[-5:]
        
    message += u"""\
Mit freundlichen Grüßen

Ihre BGHW."""

    return message
