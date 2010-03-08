# -*- coding: UTF-8 -*-
#Import der benoetigten Bibliotheken

from time import gmtime, strftime

def createtext(daten):
    """
    Bestelltext fuer Mail generieren.
    """
    gesamtpreis = 0.0
    text        = ''
    ausland     = False
    datum       = strftime("%d.%m.%Y",gmtime())

    if len(daten['Land']) > 0  or len(daten['Ustid']) > 0:
       ausland = True

    text += '\n Medienbestellung bei der BG Verkehr\n\n'

    # Angaben zum Besteller. 
    if len(daten['Mitglnr']) > 0:
        text +=  ' Mitgliedsnummer: ' + daten['Mitglnr'] + '\n\n'
    text +=  ' Absender: \n\n'
    text += ' Name:     ' + daten['VornameName'] + '\n'
    text += ' Firma:    ' + daten['Firma']   + '\n'
    text += ' Straße:   ' + daten['Strasse'] + '\n'
    text += ' Plz/Ort:  ' + daten['PlzOrt']  + '\n'
    if ausland:
        text += ' Land:     ' + daten['Land'] + '\n'
	text += ' USt-IdNr: ' + daten['Ustid'] + '\n\n'
    text += ' Telefon:  ' + daten['Telefon'] + '\n'
    text += ' Telefax:  ' + daten['Telefax'] + '\n'
    text += ' E-Mail:   ' + daten['Email']   + '\n\n'
    if daten['Abwadr']:
        text += ' Abweichende Lieferanschrift: \n\n'
        text += ' Name:     ' + daten['ALVornameName'] + '\n'
        text += ' Straße:   ' + daten['ALStrasse'] + '\n'
        text += ' Plz/Ort:  ' + daten['ALPlzOrt'] + '\n\n'

    # Bestellung
    text += ' Anzahl  Artikel\n'
  
    for artikel in daten['Bestellung']:
        text +=  '    ' + str(artikel['Anzahl']).rjust(2) + '   ' +  artikel['Artikel'] + str('%8.2f' %artikel['Preis']) + ' EUR \n'

        # Einzelpreise zusammenzaehlen
        gesamtpreis +=  artikel['Preis']

    text += '\n Gesamtbestellwert: ' + str('%8.2f' % gesamtpreis) + ' EUR ' + daten['Mwst'] + '\n\n'

    return text 


#- Test -----------------------------------------------------------------------
if __name__=='__main__':


    # Bestellte Artikel 
    bestellung = [ { 'Anzahl': 16, 'Artikel': 'Mitgliederzeitschrift "Sicherheitspartner"', 'Preis': 122.30},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
                   { 'Anzahl': 5, 'Artikel': '"Der Fahrensmann" - das Informationsblatt für die Binnenschifffahrt', 'Preis': 10.00},
              ]

    # Mehrwertsteuer aus Artikelbeschreibung
    mwst = []
    mwst.append("zzgl. Versandkosten und gesetzl. MwSt.")
    mwst.append("zzgl.  gesetzl. MwSt.")

    # Variable aus Bestellformular
    mitglnr = '123456789'
    name    = 'Hanf'
    vorname = 'Christian'
    firma   = 'Schiffko GmbH'
    strasse = 'Stubbenhuk 10'
    plz     = '12345'
    ort     = 'Hamburg'
    telefon = '1234-678900'
    telefax = '0987-6543231'
    email   = 'chanf@bgf.de'
    land    = 'Deutschland'
    ustid   = '123-456-789'
    lieferadresse = True
    lname   = 'Name der Lieferanschrift'
    lstrasse = 'Lieferstrasse 2'
    lplz    = '67890'
    lort    = 'Lieferort'

    #---------------------------------------------------------------------------
    # Besetzen Datensatz aus Bestellung
    #---------------------------------------------------------------------------
    daten = {}							    
    daten['Bestellung']  = bestellung
    daten['Mwst']        = mwst[0]
    daten['VornameName'] = vorname + ' ' + name
    daten['Mitglnr']     = mitglnr
    daten['Firma']       = firma
    daten['Strasse']     = strasse
    daten['PlzOrt']      = plz + ' ' + ort
    daten['Telefon']     = telefon
    daten['Telefax']     = telefax
    daten['Email']       = email
    daten['Land']        = land
    daten['Ustid']       = ustid
    daten['Abwadr']      = lieferadresse
    daten['ALVornameName'] = lname  # Abweichende Lieferadresse
    daten['ALStrasse']     = lstrasse
    daten['ALPlzOrt']      = lplz + ' ' + lort

    text = createtext ( daten )

    print text
