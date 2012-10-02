# -*- coding: utf-8 -*-

#Import der benoetigten Bibliotheken
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from time import gmtime, strftime
from reportlab.lib.colors import gray,black,white, red

def setcross(canvas,x,y):
        canvas.setStrokeColor(black)
        canvas.line(x*cm,y*cm,(x+0.2)*cm,(y+0.2)*cm)
        canvas.line((x+0.2)*cm,y*cm,x*cm,(y+0.2)*cm)

def settextfield(canvas,x,y,laenge,input,schriftart):
        canvas.setStrokeColor(white)
        canvas.setFillColor(white)
        canvas.rect(x*cm,y*cm,laenge*cm,0.7*cm, fill=1)
        canvas.setFillColor(black)
        canvas.setFont(schriftart, 13)
        canvas.drawString((x+0.2)*cm,(y+0.2)*cm, input)
        canvas.setFont(schriftart, 8)

def setsmalltextfield(canvas,x,y,laenge,input,schriftart):
        canvas.setStrokeColor(white)
	canvas.setFillColor(white)
        canvas.rect(x*cm,y*cm,laenge*cm,0.4*cm,fill=1)
        canvas.setFillColor(black)
        canvas.setFont(schriftart,8)
        canvas.drawString((x+0.1)*cm,(y+0.1)*cm, input)
         
def setcrossfield(canvas,x,y,schriftart):
        canvas.setStrokeColor(white)
        canvas.setFillColor(white)
        canvas.rect(x*cm,y*cm,0.4*cm,0.4*cm, fill=1)
        canvas.setFillColor(black)
        canvas.setFont(schriftart, 8)

#Definition einer Funktion

def createpdf(mytmpfile, daten):
    """
    Schreibt eine PDF-Datei
    """
    #Tests
    print daten['S1_SEM_folgetermin']
    print daten['S1_SEM_folge_von']                                                                           
    print daten['S1_SEM_folge_bis']
    #import pdb;pdb.set_trace()
    #Pfad und Dateiname

    timestamp=strftime("%d%m%Y%H%M%S",gmtime()) #Ermitteln der aktuellen Uhrzeit und Formatierung eines Strings mit Zeitstempel
    c = canvas.Canvas(mytmpfile,pagesize=A4)

    #Metainformationen fuer das PDF-Dokument
    c.setAuthor("BGHW")
    c.setTitle("Seminar-Anmeldung")

    #Variablen
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    datum = strftime("%d.%m.%Y",gmtime())

    bcp='/opt/ww4/prod_p4internet/src/bghw.seminare/bghw/seminare/lib/logo2.jpg'
    c.drawImage(bcp,2.2*cm,25.6*cm)

    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.rect(1.4*cm,1.2*cm,width=18.1*cm,height=27.2*cm)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.rect(0.2*cm,20*cm,1.6*cm,8.4*cm, fill=1)
    c.setFillColorRGB(0.91,0.91,0.92)
    c.setStrokeColorRGB(0.91,0.91,0.92)
    c.rect(0.2*cm,1.2*cm,19.3*cm,18.8*cm, fill=1)
    c.setStrokeColorRGB(0.82,0.82,0.83)
    c.setFillColorRGB(0.82,0.82,0.83)
    c.rect(1.7*cm,6.5*cm,17.8*cm,4.5*cm, fill=1)
    c.setFont(schriftartfett, 30)
    c.setFillColor(gray)
    c.drawString(4.6*cm,25.9*cm,'BGHW')
    c.setFont(schriftart, 10)
    c.drawString(4.6*cm,25.5*cm,'Berufsgenossenschaft')
    c.drawString(4.6*cm,25.1*cm,'Handel und')
    c.drawString(4.6*cm,24.7*cm,'Warendistribution')
    c.setFillColor(black)
    c.setFont(schriftartfett, 10)
    c.drawString(2.5*cm,23.7*cm, 'Doppel für  Ihre Unterlagen')
    c.setFont(schriftartfett,9)
    c.drawString(2.5*cm,23.1*cm, 'Bitte nicht an die BGHW senden oder faxen.')
    c.setFont(schriftart,8)
    c.drawString(10.9*cm,26.5*cm,'Wir beantworten gerne Ihre Fragen zum Seminarprogramm:')
    c.setFont(schriftart,8)
    c.drawString(10.9*cm,26.*cm,'Telefon 0228 5406 - 5820')
    c.drawString(10.9*cm,25.7*cm,'Telefax 0228 5406 - 5898')
    c.drawString(10.9*cm,25.3*cm,'E-Mail ausbildung@bghw.de')
    c.drawString(10.9*cm,24.9*cm,'BGHW-Prävention, Postfach 1208, 53002 Bonn')
    c.setFont(schriftart,10)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.drawString(10.9*cm,23.0*cm, '•')
    c.drawString(10.9*cm,22.7*cm, '•')
    c.setFillColor(black)
    c.setFont(schriftart,8)
    c.drawString(11.2*cm,23.0*cm,'Bitte pro Teilnehmer eine Anmeldung einreichen.')
    c.drawString(11.2*cm,22.7*cm,'Teilnahme ab 18 Jahren.')
    datum_formatiert = daten['Datum']
    c.drawString(10.9*cm,21.9*cm,'Online-Anmeldung vom %s' %datum_formatiert)
 
    #Bookinginfo
    if daten['S1_SEM_buchungsinfo']=='False':
        c.drawString(10.9*cm,21.3*cm,'Der gewünschte Termin ist ausgebucht.')
        c.drawString(10.9*cm,21.0*cm, 'Sie werden auf die Warteliste gesetzt.')

    c.setFont(schriftartfett, 15)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.drawString(1.7*cm,19.5*cm,'Online-Anmeldung')
    c.setFont(schriftart,8)
    c.setFillColor(black)
    c.drawString(1.7*cm,18.8*cm,'Die teilnehmende Person ist')
    c.drawString(2.3*cm,18.2*cm,'externe Sifa')
    c.drawString(4.7*cm,18.2*cm,'Sifa')
    c.drawString(6*cm,18.2*cm,'Unternehmer')
    c.drawString(8.6*cm,18.2*cm,'Führungskraft')
    c.drawString(11.2*cm,18.2*cm,'SiB')
    c.drawString(12.6*cm,18.2*cm,'Betriebsrat/-rätin')
    c.drawString(15.4*cm,18.2*cm,'Sonstiges')

    setcrossfield(c, 1.7, 18.2, schriftart) #externe Sifa
    setcrossfield(c, 4.1, 18.2, schriftart) #Sifa
    setcrossfield(c, 5.5, 18.2, schriftart) #Unternehmer
    setcrossfield(c, 8, 18.2, schriftart) #Führungskraft
    setcrossfield(c, 10.6, 18.2, schriftart) #SiB
    setcrossfield(c, 12, 18.2, schriftart) #Betriebsrat
    setcrossfield(c, 14.8, 18.2, schriftart) #Sonstiges
    if daten['S1_Kommtaus1']:
        setsmalltextfield(c,16.8, 18.2, 3.0, daten['S1_Kommtaus1'], schriftart)

    if daten['S1_Kommtaus'] == 'extfasi': #externe Sifa
        setcross(c,1.8,18.2)

    elif daten['S1_Kommtaus'] == 'fasi': #Sifa
        setcross(c,4.2,18.2)

    elif daten['S1_Kommtaus'] == 'unternehmer': #Unternehmer
        setcross(c,5.6,18.2)

    elif daten['S1_Kommtaus'] == 'fuehrungskraft':  #Führungskraft
        setcross(c,8.1,18.2)

    elif daten['S1_Kommtaus'] == 'sib': #SiB
        setcross(c,10.7,18.2)

    elif daten['S1_Kommtaus'] == 'betriebsrat':  #Betriebsrat
        setcross(c,12.1,18.2)

    elif daten['S1_Kommtaus'] == 'sonstiges': #Sonstiges
        setcross(c,14.9,18.2)

    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.line(1.7*cm,17.7*cm,19.5*cm,17.7*cm)
    settextfield(c, 1.7, 16.8, 7.2, daten['S1_Nachname'], schriftart)
    c.drawString(1.7*cm,16.5*cm,'Nachname')
    settextfield(c, 9.2, 16.8, 5, daten['S1_Vorname'], schriftart)
    c.drawString(9.2*cm,16.5*cm,'Vorname')
    settextfield(c, 14.5, 16.8, 5, daten['S1_Geburtsdatum'], schriftart)
    c.drawString(14.5*cm,16.5*cm,'Geburtsdatum')
    settextfield(c, 6.2, 15.5, 4, daten['S1_MGLNR'], schriftart)
    c.drawString(1.7*cm,15.5*cm,'Mitgliedsnummer (falls bekannt)')
    settextfield(c,1.7, 14.6, 18, daten['S1_Firma'], schriftart)
    c.drawString(1.7*cm,14.3*cm,'Name der Firma/Betriebsstätte (bitte nicht stempeln)')
    settextfield(c,1.7, 13.4, 7.2, daten['S1_Strasse'], schriftart)
    c.drawString(1.7*cm,13.1*cm,'Straße, Hausnummer')
    settextfield(c,9.2, 13.4, 10.3, daten['S1_PLZ'] + '  ' + daten['S1_Ort'], schriftart)
    c.drawString(9.2*cm,13.1*cm,'PLZ, Ort')
    settextfield(c,1.7, 12.2, 7.2, daten['S1_Telefon'], schriftart)
    c.drawString(1.7*cm,11.9*cm,'Telefon, Telefax')
    settextfield(c,9.2, 12.2, 10.3, daten['S1_EMail'], schriftart)
    c.drawString(9.2*cm,11.9*cm,'E-Mail')

    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.line(1.7*cm,11.8*cm,19.5*cm,11.8*cm)
    settextfield(c,1.7, 11, 17.8, daten['S1_SEM_Zeichen'], schriftart)

    c.drawString(1.7*cm,10.7*cm,'Seminar-Kurzzeichen und Seminartitel')
    settextfield(c,1.7, 9.8, 8.5, daten['S1_SEM_Ort'], schriftart)
    c.drawString(1.7*cm,9.5*cm,'Seminar-Ort')
    c.drawString(10.6*cm,10.3*cm,'Bitte wählen Sie bei gleichem Ausbildungsangebot einen')
    c.drawString(10.6*cm,9.9*cm,'Veranstaltungsort aus Ihrem Einzugsgebiet!')
    c.drawString(10.6*cm,8.85*cm,'Bitte Fahrtkostenregelung beachten.')

    c.drawString(10.6*cm, 8.3*cm, u'Übernachtung:')
    setcrossfield(c, 12.8, 8.3, schriftart)
    c.drawString(13.3*cm, 8.3*cm, u'ja')
    setcrossfield(c, 14, 8.3, schriftart)
    c.drawString(14.5*cm, 8.3*cm, u'nein')


    if daten['S1_SEM_Uebernachtung'] == 'j':
        #c.drawString(10.6*cm, 8.3*cm, 'Die Reservierung einer Übernachtungsmöglichkeit wird erbeten.')
        setcross(c, 12.9, 8.3)
    elif daten['S1_SEM_Uebernachtung'] == 'n':
        #c.drawString(10.6*cm, 8.3*cm, 'Die Reservierung einer Übernachtungsmöglichkeit ist nicht erwünscht.')
        setcross(c, 14.1, 8.3)

    c.drawString(1.7*cm,8.3*cm,'Termin von')
    settextfield(c,3.9, 8.3, 2.7, daten['S1_SEM_von'], schriftart)

    c.drawString(6.7*cm,8.3*cm,'bis')
    settextfield(c,7.3, 8.3, 2.9, daten['S1_SEM_bis'], schriftart)

    if daten['S1_SEM_folgetermin']:
        c.drawString(1.7*cm,7.3*cm,'Folgetermin von')
        settextfield(c,3.9, 7.3, 2.7,daten['S1_SEM_folge_von'][:10],schriftart)#[:10]Die ersten 10-Zeichen werden genommen.
        c.drawString(6.7*cm,7.3*cm, 'bis')
        settextfield(c,7.3, 7.3, 2.9,daten['S1_SEM_folge_bis'][:10],schriftart)#[:10]Die ersten 10-Zeichen werden genommen. 

    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.line(1.7*cm,6.5*cm,19.5*cm,6.5*cm)
    c.setFillColor(black)
    c.drawString(1.7*cm,6.1*cm,'Ansprechperson falls abweichend von oben:')
    settextfield(c,1.7, 5.2, 7.2, daten['S1_AP_Vorname'], schriftart)
    c.drawString(1.7*cm,4.9*cm,'Vorname')
    settextfield(c,9.2, 5.2, 10.3, daten['S1_AP_Nachname'], schriftart)
    c.drawString(9.2*cm,4.9*cm,'Nachname')
    settextfield(c,1.7, 4.0, 7.2, daten['S1_AP_Strasse'], schriftart)
    c.drawString(1.7*cm,3.7*cm,'Straße, Hausnummer')
    settextfield(c,9.2, 4.0, 10.3, daten['S1_AP_Ort'], schriftart)
    c.drawString(9.2*cm,3.7*cm,'PLZ, Ort')
    settextfield(c,1.7, 2.8, 7.2, daten['S1_AP_Telefax'], schriftart)
    c.drawString(1.7*cm,2.5*cm,'Telefon, Telefax')
    settextfield(c,9.2, 2.8, 10.3, daten['S1_AP_EMail'], schriftart)
    c.drawString(9.2*cm,2.5*cm,'E-Mail')

    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.line(1.7*cm,2.4*cm,19.5*cm,2.4*cm)
    c.setFont(schriftart,8)
    c.setFillColor(black)
    c.drawString(1.7*cm,2.1*cm,'Wir verpflichten uns bei unentschuldigtem Fernbleiben oder der Nichtinanspruchnahme der gebuchten Übernachtung/en etc. oder ')
    c.drawString(1.7*cm,1.8*cm,'unbegründeter vorzeitiger Abreise zur Zahlung der anfallenden Kosten. Die Anfrage stützt sich auf § 192 Abs. 3 SGB VII. Die Daten werden')
    c.drawString(1.7*cm,1.5*cm,'entsprechend datenschutzrechtlicher Bestimmungen behandelt.')

    c.showPage()

    #bei allen Nicht-Fasi-Seminaren wird die 2. Seite nicht gedruckt
    if not daten['S2_Strasse'] and not daten['S2_PLZ'] and not daten['S2_Ort']:
        c.save()
        return

    c.setStrokeColorRGB(0.91,0.91,0.92)
    c.setFillColorRGB(0.91,0.91,0.92)
    c.rect(0.2*cm,1.5*cm,19.3*cm,27.2*cm, fill=1)
    c.setFont(schriftartfett, 15)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.drawString(1.7*cm,28*cm,'Anmeldung zur Sifa-Ausbildung P I und P V')
    c.setFillColor(black)
    c.setFont(schriftart, 8)
    c.drawString(12.3*cm,27*cm,'Als Fachkräfte für Arbeitssicherheit (Sifa) dürfen')
    c.drawString(12.3*cm,26.6*cm,'Personen nur bestellt werden, die im Jahr regelmäßig')
    c.drawString(12.3*cm,26.2*cm,'gemäß der Unfallverhütungsvorschrift DGUV Vorschrift 2')
    c.drawString(12.3*cm,25.8*cm,'als solche tätig sind und bestimmte berufliche Voraus-')
    c.drawString(12.3*cm,25.4*cm,'setzungen erfüllen. Zusätzlich müssen die betreffenden')
    c.drawString(12.3*cm,25*cm,'Personen den Nachweis der sicherheitstechnischen')
    c.drawString(12.3*cm,24.6*cm,'Fachkunde erbringen. Diese Fachkunde wird in berufs-')
    c.drawString(12.3*cm,24.2*cm,'genossenschaftlichen Ausbildungslehrgängen ver-')
    c.drawString(12.3*cm,23.8*cm,'mittelt. Wir prüfen, ob die angemeldete Person')
    c.drawString(12.3*cm,23.4*cm,'die Voraussetzungen erfüllt, daher bitten wir um die')
    c.drawString(12.3*cm,23*cm,'nachstehenden Angaben.')



    settextfield(c, 1.7, 26.5, 9.7, daten['S2_Nachname'], schriftart)
    c.drawString(1.7*cm,26*cm,'Nachname')
    settextfield(c, 1.7, 25, 9.7, daten['S2_Vorname'], schriftart)
    c.drawString(1.7*cm,24.5*cm,'Vorname')
    settextfield(c, 1.7, 23.5, 9.7, daten['S2_Strasse'], schriftart)
    c.drawString(1.7*cm,23*cm,'privater Wohnort (Straße, PLZ, Ort)')
    settextfield(c, 1.7, 22, 9.7, daten['S2_PLZ']+' '+daten['S2_Ort'], schriftart)
    settextfield(c, 1.7, 21, 9.7, ' ', schriftart)
    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.line(1.7*cm,20.2*cm,19.5*cm,20.2*cm)
    c.setFont(schriftartfett, 12)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.drawString(1.7*cm,19.3*cm,'Allgemeine Ausbildungsvoraussetzung')
    c.setFont(schriftart, 10)
    c.drawString(9.9*cm,19.3*cm,'(Präsenzphase P I)')
    c.setFillColor(black)
    c.setFont(schriftart, 8)
    c.drawString(1.7*cm,18.7*cm,'Wie viele Mitarbeiter (Vollarbeiter - Umrechnung gemaess Arbeitsschutzgesetz)' )
    settextfield(c, 14, 18.4, 1.4, daten['S2_anzahl_mitarbeiter'], schriftart)
    c.drawString(1.7*cm,18.3*cm,'wird die angemeldete Person zukünftig als Sifa betreuen?')
    c.drawString(1.7*cm,17.7*cm,'Wird die angemeldete Person mindestens 50 Arbeitsstunden im Jahr' )
    c.drawString(1.7*cm,17.3*cm,'regelmäßig als Fachkraft für Arbeitssicherheit tätig werden?')
    c.drawString(14.5*cm,17.3*cm,'ja')
    c.drawString(16*cm,17.3*cm,'nein')
    setcrossfield(c, 14, 17.3, schriftart) #mitarbeiter taetig ja
    setcrossfield(c, 15.5, 17.3, schriftart) #mitarbeiter teaetig nein

    if daten['S2_voraussetzungen_mitarbeiter_taetig'] == 'ja':
        setcross(c,14.1,17.3)

    elif daten['S2_voraussetzungen_mitarbeiter_taetig'] == 'nein':
        setcross(c,15.7,17.3)

    c.drawString(1.7*cm, 16.7*cm, 'Wurde die Anmeldung mit dem zuständigen Technischen Aufsichtsbeamten(TAB) besprochen?')
    c.drawString(14.5*cm,16.7*cm,'ja')
    c.drawString(16*cm,16.7*cm,'nein')
    setcrossfield(c, 14, 16.7, schriftart) #tab besprochen ja
    setcrossfield(c, 15.5, 16.7, schriftart) #tab besprochen nein

    if daten['S2_tab_besprochen'] == 'ja':
       setcross(c,14.1,16.7)
    elif daten['S2_tab_besprochen'] == 'nein':
       setcross(c,15.6,16.7)

    #Zeichnen einer Linie
    c.setStrokeColorRGB(0.82,0.82,0.83)
    c.line(1.7*cm,15.2*cm,19.5*cm,15.22*cm)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.setFont(schriftartfett, 12)
    c.drawString(1.7*cm,14.4*cm,'Berufliche Voraussetzung')
    c.setFont(schriftart, 10)
    c.drawString(7.2*cm,14.4*cm,'(§ 4 Abs. 2 - 5 DGUV Vorschrift 2)')
    c.setFillColor(black)
    c.setFont(schriftart, 8)
    c.drawString(2.2*cm,13.7*cm,'Ingenieur/in oder')
    c.drawString(2.2*cm,13.4*cm,'gleichwertige Ausbildung') 
    c.drawString(7.7*cm,13.7*cm,'Techniker/in')
    c.drawString(10.7*cm,13.7*cm,'Meister/in')
    setcrossfield(c, 1.7, 13.7, schriftart) 
    setcrossfield(c, 7.2, 13.7, schriftart) 
    setcrossfield(c, 10.2, 13.7, schriftart)    

    if daten['S2_job'] == 'ingenieur':#Ingeneur
        setcross(c,1.8,13.7)

    elif daten['S2_job'] == 'techniker':#Techniker
        setcross(c,7.3,13.7)

    elif daten['S2_job'] == 'meister':#Meister
        setcross(c,10.3,13.7)

    c.drawString(12.7*cm,13.7*cm,'Als solche/r')
    if not daten['S2_taetig_als']:
        settextfield(c, 14.7, 13.7, 1, daten['S2_jahre_taetig1'], schriftart) #Als solcher x Jahre tätig
    else:    
        settextfield(c, 14.7, 13.7, 1, '', schriftart) #Als solcher x Jahre tätig
    c.drawString(16*cm,13.7*cm, 'Jahre tätig.')
    c.drawString(1.7*cm,12.7*cm,'Ohne Meisterprüfung als Meister/in oder in gleichwertiger Funktion' )
    if daten['S2_taetig_als']:
        settextfield(c, 10.1, 12.7, 1, daten['S2_jahre_taetig2'], schriftart) #Als solcher x Jahre tätig
    else:    
        settextfield(c, 10.1, 12.7, 1, '', schriftart) #Als solcher x Jahre tätig
    c.drawString(11.2*cm,12.7*cm, 'Jahre tätig als:')
    settextfield(c, 13.2, 12.7, 6, daten['S2_taetig_als'], schriftart) #tätig als
    c.setStrokeColorRGB(0.82,0.82,0.83)
    c.line(1.7*cm,12*cm,19.5*cm,12*cm)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.setFont(schriftartfett, 12)
    c.drawString(1.7*cm,11*cm,'Bestellung der angemeldeten Person zur Fachkraft für Arbeitssicherheit')

    c.setFillColor(black)
    c.setFont(schriftart, 8)
    c.drawString(2.2*cm,10*cm,'Dies wurde mit dem Betriebsrat besprochen.')
    c.drawString(10*cm,10*cm,'Es existiert kein Betriebsrat im Unternehmen.')
    c.drawString(2.2*cm,9.4*cm,'Zur Zeit keine Angabe möglich.')
    setcrossfield(c, 1.7, 10, schriftart) #Betriebsrat Ja
    setcrossfield(c, 9.5, 10, schriftart) #Betriebsrat Nein
    setcrossfield(c, 1.7, 9.4, schriftart) #Zur Zeit keine Angabe möglich    

    if daten['S2_betriebsrat'] == 'betriebsrat':
        setcross(c,1.8,10)
    elif daten['S2_betriebsrat'] == 'kein_betriebsrat':
        setcross(c,9.6,10)
    elif daten['S2_betriebsrat'] == 'ka':
        setcross(c,1.8,9.5)

    c.setStrokeColorRGB(0.0,0.29,0.58)
    c.line(1.7*cm,9*cm,19.5*cm,9*cm)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.setFont(schriftartfett, 12)
    c.drawString(1.7*cm,8*cm,'Branchenspezifische Ausbildung')
    c.setFont(schriftart, 10)
    c.drawString(8.7*cm,8*cm,'(Präsenzphase P V)')
    c.setFillColor(black)
    c.setFont(schriftart, 8)
    c.drawString(2*cm,6.5*cm,'Die angemeldete Person hat an der Sifa-Ausbildung (inkl. Abschluss von P IV)')
    c.drawString(2*cm,6*cm,'bei der BGHW mit Erfolg teilgenommen.')
    setcrossfield(c, 12.4, 6, schriftart) 

    if daten['S2_ausbildung'] == "bghw":
        setcross(c,12.5,6)

    c.drawString(2*cm,5*cm,'Die angemeldete Person hat an der Sifa-Ausbildung (inkl. Abschluss von P IV) eines')
    c.drawString(2*cm,4.5*cm,'anderen Veranstalters mit Erfolg teilgenommen - bitte Nachweis beilegen.')
    c.drawString(2*cm,3.5*cm,'Die angemeldete Person ist Mitarbeiter/in eines sicherheitstechnischen Dienstes')
    setcrossfield(c, 12.4, 4.5, schriftart)
    setcrossfield(c, 12.4, 3.5, schriftart)

    if daten['S2_ausbildung'] == "veranstalter":
        setcross(c,12.5, 4.5)

    if daten['S2_ausbildung'] == "svd":
        setcross(c,12.5, 3.5)
   
    c.setFont(schriftart,10)
    c.setFillColorRGB(0.0,0.29,0.58)
    c.drawString(1.7*cm,6.5*cm, '•')
    c.drawString(1.7*cm,5*cm, '•')
    c.drawString(1.7*cm,3.5*cm, '•')
    c.setFillColor(black)

    #Zeichnen einer Linie
    c.setStrokeColorRGB(0.82,0.82,0.83)
    c.line(1.7*cm,3*cm,19.5*cm,3*cm)
    
    c.setFont(schriftart, 7)
    c.drawString(1.7*cm,2.2*cm,'Die Anfrage stützt sich auf § 192 Abs.3 SGB VII in Verbindung mit § 13 Abs.1 ASiG.')
    c.drawString(1.7*cm,1.8*cm,'Die Daten werden entsprechend datenschutzrechtlicher Bestimmungen behandelt.')

    c.showPage()
    c.save()
    return
