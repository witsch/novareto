# -*- coding: utf-8 -*-

def createMessage(data):
    message = """\
Das ist die Bestellung des Mitgliedsbetriebes:
"""
    for i in data.get('bestellung'):
        message += """\
Artikelnummer:  %s
Bezeichnung:    %s
Menge:          %s

""" % (i.artikel, i.beschreibung, i.anzahl)

    message += """\
Mitgliedsnummer:    %s
Firma:              %s
Titel:              %s
Anrede:             %s
Vorname:            %s
Name:               %s

""" % (data.get('mitgliedsnummer'),
       data.get('firma'),
       data.get('titel'),
       data.get('anrede'),
       data.get('vorname'),
       data.get('name'),)
    print message
    return message
