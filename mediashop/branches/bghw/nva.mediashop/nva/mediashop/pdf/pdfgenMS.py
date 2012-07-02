# -*- coding: UTF-8 -*-
#Import der benoetigten Bibliotheken
import socket
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from time import gmtime, strftime
from reportlab.lib.colors import gray
from reportlab.platypus.frames import Frame
from reportlab.platypus import Table
from reportlab.graphics.barcode.code128 import Code128
from reportlab.graphics.barcode.code39 import Standard39
from reportlab.graphics.barcode.code39 import Extended39
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT as _r

#Variablen
schriftart = "Helvetica"
courier = "Courier"
courierfett = "Courier-Bold"
schriftartfett = "Helvetica-Bold"
datum = strftime("%d.%m.%Y",gmtime())


def splitline (line):
    """ Wenn Zeile groesser 45 Char, aufsplitten in 2 Zeilen """
    maxchar = 45
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


def kopf (c, count=0):
    '''
    Kopf: Ueberschrift, Logo, Trennlinie

    Achtung: Pfad fuer 'Logo' anpassen
    '''
    bcp = '/'.join(__file__.split('/')[:-1])+"/bghwlogo_bearbeitet.jpg"
    
    c.drawImage(bcp,13*cm,26.7*cm,width=3.74*cm,height=1.55*cm)

    # Adressfeld
    c.setFont(schriftart, 12)
    c.drawString( 2.2*cm, 24.1*cm, 'Berufsgenossenschaft')
    c.drawString( 2.2*cm, 23.6*cm, 'Handel und Warendistribution')
    c.drawString( 2.2*cm, 23.1*cm, 'Direktion Bonn')
    c.drawString( 2.2*cm, 22.6*cm, 'Prävention')
    c.drawString( 2.2*cm, 22.1*cm, 'Niebuhrstraße 5')
    c.drawString( 2.2*cm, 21.6*cm, '53113 Bonn')

    c.drawString(16.8*cm, 20.0*cm, datum)

    c.setFont(schriftartfett, 12)
    c.drawString(12.3*cm, 24.1*cm, 'Kontakt:')
    c.setFont(schriftart, 12)
    c.drawString(12.3*cm, 23.6*cm, 'E-Mail: %s' %'medien@bghw.de')
    c.drawString(12.3*cm, 23.1*cm, 'Telefon: %s' %'0228-')
    c.drawString(12.3*cm, 22.6*cm, 'Telefax: %s' %'0228-')

    # Betreff
    c.setFont(schriftartfett, 12)
    randint = random.randint(100, 999)
    bestellnummer = "%s-%s-%s-%s" %(socket.gethostname()[-1], strftime("%y%m%d%H%M",gmtime()), randint, count)

    text = 'Online-Bestellung Nr.: %s vom: %s' %(bestellnummer, datum)
    c.drawString( 2.2*cm, 19.0*cm, text)


def chunks(thing, chunk_length):
    """Iterate through thing in chunks of size chunk_length.

    Note that the last chunk can be smaller than chunk_length.
    """
    for i in xrange(0, len(thing), chunk_length):
        yield thing[i:i+chunk_length]


#Definition einer Funktion
def createpdf (filename, daten):
    """
    Schreibt eine PDF-Datei
    """
    ausland = False
    if len(daten['Land']) > 0  or len(daten['Ustid']) > 0:
       ausland = True

    # Pfad und Dateiname

    #c ist ein Objekt der Klasse Canvas
    c = canvas.Canvas(filename,pagesize=A4)

    #Metainformationen fuer das PDF-Dokument
    c.setAuthor("Lars Walther, novareto GmbH")
    c.setTitle("BGHW")

    kopf(c)

    # Angaben zu den ausgesuchten Artikeln
    offset      = -0.6
    gesamtpreis = 0.0
    c.setFont(schriftartfett, 10)
    c.drawString( 2.2*cm, 17.5*cm, u'Artikel-Code')
    c.drawString( 6.2*cm, 17.5*cm, u'Artikel')
    c.drawString( 13.5*cm, 17.5*cm, u'Menge')
    c.drawString( 14.9*cm, 17.5*cm, u'Einzelpreis(EUR)')
    c.drawString(18.1*cm, 17.5*cm, u'Preis(EUR)')
  
    c.setLineWidth (0.5) 
    c.line(2.2*cm,17.3*cm,20*cm,17.3*cm)

    count = 0
    for artikel in daten['Bestellung']:
        offset += 0.6
        c.setFont(courier, 10) #Proportionalschrift

        #Noch steht nicht fest welcher Barcode verwendet werden soll.
        #bc = Code128(value = artikel['PseudoEan'].replace(' ',''), barWidth = 1.0, barHeight = 12, lquiet = 5, rquiet = 5)
        bc = Standard39(artikel['Artikelnummer'], barWidth = 1.0, barHeight = 12)

        bc.drawOn(c, 2*cm, (16.6-offset)*cm)
        c.drawString(13.5*cm, (16.7-offset)*cm, str(artikel['Anzahl']).rjust(2))
        einzelpreis = artikel['Preis'] / artikel['Anzahl']
        c.drawString(15.1*cm, (16.7-offset)*cm, str('%8.2f' %einzelpreis))
        c.drawString(17.8*cm, (16.7-offset)*cm, str('%8.2f' %artikel['Preis']))

        #c.setFont(schriftart, 12)
        #c.drawString(16.0*cm, (16.7-offset)*cm, 'EUR')

        # Einzelpreise zusammenzaehlen
        gesamtpreis +=  artikel['Preis']

        # Die Artikelbeschreibung kann ueber mehrere Zeilen gehen
        c.setFont(schriftart,10)
        text_artikel = splitline(artikel['Artikel'])
        offset_text = 0.0
        for zeile in text_artikel:
            offset += offset_text
            c.drawString( 6.2*cm, (16.7-offset)*cm, zeile)
            offset_text = 0.4
   
        c.setLineWidth (0.5) 
        c.line(2.2*cm,(16.55-offset)*cm,20*cm,(16.55-offset)*cm)
     
        # Neue Seite, wenn Seite voll
        if offset > 10.0:
            count+=1
            c.showPage()
            kopf(c, count)
            offset = -11.5

    c.setFont(schriftart, 12)
    c.drawString( 2.2*cm, (15.5-offset)*cm, 'Gesamtbestellwert:')
    c.setFont(schriftartfett, 12)
    c.drawString( 6.5*cm, (15.5-offset)*cm, 'EUR')
    c.drawString( 7.5*cm, (15.5-offset)*cm, str('%8.2f' % gesamtpreis))
    c.setFont(schriftart, 12)
    c.drawString( 9.3*cm, (15.5-offset)*cm, daten['Mwst'])

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
        count+=1
        c.drawString(11.5*cm, 2.0*cm, 'Absender/Lieferadresse auf Folgeseite.')
        c.showPage()
        kopf(c, count)
        offset = -11.0

    # Angaben zum Besteller. 
    c.setFont(schriftartfett, 12)
    c.drawString( 2.2*cm, (14.5-offset)*cm, 'Absender:')
    c.setFont(schriftart, 10)
    if len(daten['Mitglnr']) > 0:
        c.drawString( 2.2*cm, (13.9-offset)*cm, 'Mitgliedsnummer:')
    c.drawString( 2.2*cm, (13.4-offset)*cm, 'Name:')
    c.drawString( 2.2*cm, (12.9-offset)*cm, 'Firma:')
    c.drawString( 2.2*cm, (12.4-offset)*cm, 'Straße:')
    c.drawString( 2.2*cm,  (11.9-offset)*cm, 'Plz/Ort:')

    c.drawString(11.5*cm, (12.9-offset)*cm, 'Telefon:')
    c.drawString(11.5*cm, (12.4-offset)*cm, 'Telefax:')
    c.drawString(11.5*cm,  (11.9-offset)*cm, 'E-Mail:')

    c.setFont(schriftart, 10)
    c.drawString( 5.5*cm, (13.9-offset)*cm, daten['Mitglnr'])
    c.drawString( 4.5*cm, (13.4-offset)*cm, daten['VornameName'])
    c.drawString( 4.5*cm, (12.9-offset)*cm, daten['Firma'])
    c.drawString( 4.5*cm, (12.4-offset)*cm, daten['Strasse'])
    c.drawString( 4.5*cm,  (11.9-offset)*cm, daten['PlzOrt'])

    c.drawString(13.0*cm, (12.9-offset)*cm, daten['Telefon'])
    c.drawString(13.0*cm, (12.4-offset)*cm, daten['Telefax'])
    c.drawString(13.0*cm,  (11.9-offset)*cm, daten['Email'])
        
    if ausland:
        c.setFont(schriftart, 10)
        c.drawString( 2.2*cm,  (11.4-offset)*cm, 'Land:')
        c.drawString( 2.2*cm,  (10.9-offset)*cm, 'USt-IdNr/VAT:')
        c.setFont(schriftart, 12)
        c.drawString( 4.5*cm,  (11.4-offset)*cm, daten['Land'])
        c.drawString( 5.5*cm,  (10.9-offset)*cm, daten['Ustid'])
        offset += 1.0

    if daten['Abwadr']:
        c.setFont(schriftartfett, 12)
        c.drawString( 2.2*cm, (10.9-offset)*cm, 'Abweichende Lieferanschrift:')
        c.setFont(schriftart, 10)
        c.drawString( 2.2*cm, (10.3-offset)*cm, 'Firma:')
        c.drawString( 2.2*cm, (9.8-offset)*cm, 'Name:')
        c.drawString( 2.2*cm, (9.3-offset)*cm, 'Straße:')
        c.drawString( 2.2*cm, (8.8-offset)*cm, 'Plz/Ort:')
        c.setFont(schriftart, 12)
        c.drawString( 4.5*cm, (10.3-offset)*cm, daten['ALFirma'])
        c.drawString( 4.5*cm, (9.8-offset)*cm, daten['ALVornameName'])
        c.drawString( 4.5*cm, (9.3-offset)*cm, daten['ALStrasse'])
        c.drawString( 4.5*cm, (8.8-offset)*cm, daten['ALPlzOrt'])
        offset += 2.6

    #Seitenumbruch
    c.showPage()

    #Schliessen der Datei
    c.save()

    fp = open(filename,'r')
    c  = fp.read()

    fp.close()

    return c

