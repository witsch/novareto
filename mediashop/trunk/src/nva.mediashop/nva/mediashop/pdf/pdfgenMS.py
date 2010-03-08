# -*- coding: UTF-8 -*-
#Import der benoetigten Bibliotheken
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from time import gmtime, strftime
from reportlab.lib.colors import gray

def splitline (line):
    """ Wenn Zeile groesser 50 Char, aufsplitten in 2 Zeilen """
    maxchar = 55
    zeilen  = []
    zeile   = ''

    woerter = line.split( ' ')
    for wort in woerter:
        if (len(zeile)+len(wort)) > maxchar:
            zeilen.append(zeile)
            zeile = ''

        zeile += wort + ' '

    if zeile != '':
        zeilen.append(zeile)

    return zeilen


def kopf (c):
    '''
    Kopf: Ueberschrift, Logo, Trennlinie

    Achtung: Pfad fuer 'Logo' anpassen
    '''
    #bcp="./src/nva.mediashop/nva/mediashop/pdf/Logo-BG-Verkehr-schwarz-2z.png"
    #bcp="/Users/cklinger/work/bgf/mshop/src/nva.mediashop/nva/mediashop/pdf/Logo-BG-Verkehr-schwarz-2z.png"
    bcp = '/'.join(__file__.split('/')[:-1])+"/Logo-BG-Verkehr-schwarz-2z.png"
    
    c.drawImage(bcp,13*cm,26.7*cm,width=6.00*cm,height=1.55*cm)

    c.setLineWidth (1) 
    c.line(2.5*cm,26.5*cm,19.0*cm,26.5*cm)


#Definition einer Funktion
def createpdf (filename, daten):
    """
    Schreibt eine PDF-Datei
    """
    ausland = False
    if len(daten['Land']) > 0  or len(daten['Ustid']) > 0:
       ausland = True

    #---------------------------------------------------------------------------
    # Pfad und Dateiname

    #c ist ein Objekt der Klasse Canvas
    c = canvas.Canvas(filename,pagesize=A4)

    #Metainformationen fuer das PDF-Dokument
    c.setAuthor ("Christian Hanf")
    c.setTitle  ("BG Verkehr")

    #Variablen 
    schriftart     = "Helvetica"
    courier        = "Courier-Bold"
    schriftartfett = "Helvetica-Bold"

    datum          = strftime("%d.%m.%Y",gmtime())

    kopf(c)

    # Adressfeld
    c.setFont(schriftartfett, 15)
    c.drawString(14.0*cm, 24.5*cm, 'Fax.: 040 3980-1040')

    c.setFont(schriftart, 12)
    c.drawString( 2.5*cm, 24.5*cm, 'An die')
    c.drawString( 2.5*cm, 24.1*cm, 'Vertriebsgesellschaft für Medien der BG Verkehr')
    c.drawString( 2.5*cm, 23.7*cm, 'GSV Gmbh')
    c.drawString( 2.5*cm, 23.3*cm, 'Ottenser Hauptstraße 54')
    c.drawString( 2.5*cm, 22.9*cm, '22765 Hamburg')

    c.drawString(16.8*cm, 20.0*cm, datum)

    # Betreff
    c.setFont(schriftartfett, 12)
    c.drawString( 2.5*cm, 19.0*cm, 'Medienbestellung bei der BG Verkehr')

    # Anschreiben
    c.setFont(schriftart,12)
    c.drawString( 2.5*cm, 17.5*cm, 'Sehr geehrte Damen und Herren,')
    c.drawString( 2.5*cm, 16.7*cm, 'ich bitte um Zusendung von:')

    # Angaben zu den ausgesuchten Artikeln
    offset      = -0.6
    gesamtpreis = 0.0
    c.setFont(schriftartfett, 10)
    c.drawString( 2.5*cm, 15.5*cm, 'Anzahl')
    c.drawString( 4.0*cm, 15.5*cm, 'Artikel')
    c.drawString(17.0*cm, 15.5*cm, 'Bestellwert')
  
    c.setLineWidth (0.5) 
    c.line(2.5*cm,15.3*cm,19.0*cm,15.3*cm)

    for artikel in daten['Bestellung']:
        offset += 0.6
        c.setFont(courier, 14)                            #  Proportionalschrift
        c.drawString( 2.8*cm, (14.7-offset)*cm, str(artikel['Anzahl']).rjust(2))
        c.drawString(16.6*cm, (14.7-offset)*cm, str('%8.2f' %artikel['Preis']))

        c.setFont(schriftart, 12)
        c.drawString(16.0*cm, (14.7-offset)*cm, 'EUR')

        # Einzelpreise zusammenzaehlen
        gesamtpreis +=  artikel['Preis']

        # Die Artikelbeschreibung kann ueber mehrere Zeilen gehen
        text_artikel = splitline(artikel['Artikel'])
        offset_text = 0.0
        for zeile in text_artikel:
            offset += offset_text
            c.drawString( 4.0*cm, (14.7-offset)*cm, zeile)
            offset_text = 0.4
   
        c.setLineWidth (0.5) 
        c.line(2.5*cm,(14.55-offset)*cm,19.0*cm,(14.55-offset)*cm)
     
        # Neue Seite, wenn Seite voll
        if offset > 10.0:
            c.showPage()
            kopf(c)
            offset = -11.5

    c.setFont(schriftart, 12)
    c.drawString( 2.5*cm, (13.5-offset)*cm, 'Gesamtbestellwert:')
    c.setFont(schriftartfett, 12)
    c.drawString( 6.5*cm, (13.5-offset)*cm, 'EUR')
    c.drawString( 7.5*cm, (13.5-offset)*cm, str('%8.2f' % gesamtpreis))
    c.setFont(schriftart, 12)
    c.drawString( 9.3*cm, (13.5-offset)*cm, daten['Mwst'])

    # Passt Anschrift noch auf Seite? Sonst neue Seite.
    neueSeite = False

    if offset > 5.5:
        neueSeite = True
    if offset > 4.5 and ausland:
        neueSeite = True
    if offset > 3.0 and daten['Abwadr']:
        neueSeite = True
    if offset > 2.0 and ausland and daten['Abwadr']:
        neueSeite = True
     
    if neueSeite:
  
        c.drawString(11.5*cm, 2.0*cm, 'Absender/Lieferadresse auf Folgeseite.')
        c.showPage()
        kopf(c)
        offset = -11.0

    # Angaben zum Besteller. 
    c.setFont(schriftartfett, 12)
    c.drawString( 2.5*cm, (12.5-offset)*cm, 'Absender:')
    c.setFont(schriftart, 10)
    if len(daten['Mitglnr']) > 0:
        c.drawString( 2.5*cm, (11.9-offset)*cm, 'Mitgliedsnummer:')
    c.drawString( 2.5*cm, (11.4-offset)*cm, 'Name:')
    c.drawString( 2.5*cm, (10.9-offset)*cm, 'Firma:')
    c.drawString( 2.5*cm, (10.4-offset)*cm, 'Straße:')
    c.drawString( 2.5*cm,  (9.9-offset)*cm, 'Plz/Ort:')

    c.drawString(11.5*cm, (10.9-offset)*cm, 'Telefon:')
    c.drawString(11.5*cm, (10.4-offset)*cm, 'Telefax:')
    c.drawString(11.5*cm,  (9.9-offset)*cm, 'E-Mail:')

    c.setFont(schriftart, 12)
    c.drawString( 5.5*cm, (11.9-offset)*cm, daten['Mitglnr'])
    c.drawString( 4.5*cm, (11.4-offset)*cm, daten['VornameName'])
    c.drawString( 4.5*cm, (10.9-offset)*cm, daten['Firma'])
    c.drawString( 4.5*cm, (10.4-offset)*cm, daten['Strasse'])
    c.drawString( 4.5*cm,  (9.9-offset)*cm, daten['PlzOrt'])

    c.drawString(13.0*cm, (10.9-offset)*cm, daten['Telefon'])
    c.drawString(13.0*cm, (10.4-offset)*cm, daten['Telefax'])
    c.drawString(13.0*cm,  (9.9-offset)*cm, daten['Email'])
        
    if ausland:
        c.setFont(schriftart, 10)
        c.drawString( 2.5*cm,  (9.4-offset)*cm, 'Land:')
        c.drawString( 2.5*cm,  (8.9-offset)*cm, 'USt-IdNr:')
        c.setFont(schriftart, 12)
        c.drawString( 4.5*cm,  (9.4-offset)*cm, daten['Land'])
        c.drawString( 4.5*cm,  (8.9-offset)*cm, daten['Ustid'])
        offset += 1.0

    if daten['Abwadr']:
        c.setFont(schriftartfett, 12)
        c.drawString( 2.5*cm, (8.9-offset)*cm, 'Abweichende Lieferanschrift:')
        c.setFont(schriftart, 10)
        c.drawString( 2.5*cm, (8.3-offset)*cm, 'Name:')
        c.drawString( 2.5*cm, (7.8-offset)*cm, 'Straße:')
        c.drawString( 2.5*cm, (7.3-offset)*cm, 'Plz/Ort:')
        c.setFont(schriftart, 12)
        c.drawString( 4.5*cm, (8.3-offset)*cm, daten['ALVornameName'])
        c.drawString( 4.5*cm, (7.8-offset)*cm, daten['ALStrasse'])
        c.drawString( 4.5*cm, (7.3-offset)*cm, daten['ALPlzOrt'])
        offset += 2.6

    c.setFont(schriftartfett, 12)
    c.drawString( 2.5*cm, (7.9-offset)*cm, 'Unterschrift:')
 
    #Seitenumbruch
    c.showPage()

    #Schliessen der Datei
    c.save()

    fp = open(filename,'r')
    c  = fp.read()

    fp.close()

    return c


#- Test -----------------------------------------------------------------------
if __name__=='__main__':

    filename = '/tmp/medienshop.pdf'

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

    test = createpdf (filename, daten )
