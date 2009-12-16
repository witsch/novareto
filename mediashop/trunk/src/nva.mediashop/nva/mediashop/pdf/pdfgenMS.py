# -*- coding: UTF-8 -*-
#Import der benoetigten Bibliotheken
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from time import gmtime, strftime
from reportlab.lib.colors import gray

def splitline (line):
    """ Wenn Zeile groesser 50 Char, aufsplitten in 2 Zeilen """
    maxchar = 50
    zeilen  = []
    zeile   = ''

    woerter = line.split( ' ')
    for wort in woerter:
        zeile += wort + ' '
        if len(zeile) > maxchar:
            zeilen.append(zeile)
            zeile = ''

    if zeile != '':
        zeilen.append(zeile)

    return zeilen

def kopf (c):
    '''
    Kopf: Ueberschrift, Logo, Trennlinie

    Achtung: Pfad fuer 'Logo' anpassen
    '''
   # bcp="/opt/plone/plone/products/Registrierung/lib/Logo-BG-Verkehr-schwarz-2z.png"
    #bcp="/opt/plone/medienshop/src/nva.mediashop/nva/mediashop/pdf/Logo-BG-Verkehr-schwarz-2z.png"
    bcp="/Users/cklinger/work/bgf/mshop/src/nva.mediashop/nva/mediashop/pdf/Logo-BG-Verkehr-schwarz-2z.png"

    c.drawImage(bcp,13*cm,26.7*cm,width=6.00*cm,height=1.55*cm)

    c.setLineWidth (1) 
    c.line(2.5*cm,26.5*cm,19.0*cm,26.5*cm)


#Definition einer Funktion
def createpdf (filename, daten):
    """
    Schreibt eine PDF-Datei
    """

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
    c.drawString( 2.5*cm, 24.5*cm, 'An')
    c.drawString( 2.5*cm, 24.1*cm, 'Vertriebsgesellschaft für BG-Medien')
    c.drawString( 2.5*cm, 23.7*cm, 'G S V')
    c.drawString( 2.5*cm, 23.3*cm, 'Ottenser Hauptstraße 54')
    c.drawString( 2.5*cm, 22.9*cm, '22765 Hamburg')

    c.drawString(16.8*cm, 20.0*cm, datum)

    # Betreff
    c.setFont(schriftartfett, 12)
    c.drawString( 2.5*cm, 19.0*cm, 'Mein Bestellschein aus dem BG Verkehr Medienkatalog')

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

    # Angaben zum Besteller. Neue Seite, wenn Seite voll
    if offset > 7.0:
        c.showPage()
        kopf(c)
        offset = -11.0

    c.setFont(schriftartfett, 12)
    c.drawString( 2.5*cm, (12.3-offset)*cm, 'Absender:')
    c.setFont(schriftart, 10)
    c.drawString( 2.5*cm, (11.7-offset)*cm, 'Mitgliedsnummer:')
    c.drawString( 2.5*cm, (11.2-offset)*cm, 'Name:')
    c.drawString( 2.5*cm, (10.7-offset)*cm, 'Firma:')
    c.drawString( 2.5*cm, (10.2-offset)*cm, 'Straße:')
    c.drawString( 2.5*cm,  (9.7-offset)*cm, 'Plz/Ort:')
    c.drawString(12.5*cm, (10.7-offset)*cm, 'Telefon:')
    c.drawString(12.5*cm, (10.2-offset)*cm, 'Telefax:')
    c.drawString(12.5*cm,  (9.7-offset)*cm, 'E-Mail:')
    c.setFont(schriftart, 12)
    c.drawString( 5.5*cm, (11.7-offset)*cm, daten['Mitglnr'])
    c.drawString( 4.5*cm, (11.2-offset)*cm, daten['VornameName'])
    c.drawString( 4.5*cm, (10.7-offset)*cm, daten['Firma'])
    c.drawString( 4.5*cm, (10.2-offset)*cm, daten['Strasse'])
    c.drawString( 4.5*cm,  (9.7-offset)*cm, daten['PlzOrt'])
    c.drawString(14.5*cm, (10.7-offset)*cm, daten['Telefon'])
    c.drawString(14.5*cm, (10.2-offset)*cm, daten['Telefax'])
    c.drawString(14.5*cm,  (9.7-offset)*cm, daten['Email'])

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
