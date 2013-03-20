# -*- coding: utf-8 -*-
# @author: Lars Walther

#Import der benoetigten Bibliotheken
from time import gmtime, strftime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import grey

from reportlab.platypus.frames import Frame
from reportlab.platypus import Table
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT as _r
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate

from nva.onlinehandlungshilfe.lib.helpers import valuegetter
from nva.bsbetreuung.lib.helpers import formatFragen, formatAufgaben

#Try/Excepts fuer Tests
try:
    from zope.i18n import translate
except:
    def translate(text, target_language):
        return text
try:        
    from uv.onlinehandlungshilfe import uvhandlungshilfeMessageFactory as _
except:
    def _(text):
        return text


def mainPageFrame(canvas, doc):

    canvas.saveState()
    canvas.setFont('Helvetica', 12)
    #canvas.Canvas(tmpfile,pagesize=landscape(A4))
    canvas.setAuthor("BG Energie Textil Elektro Medienerzeugnisse")
    canvas.setTitle("DGUV Vorschrift 2 - Online Handlungshilfe")
    canvas.restoreState()



class HHTemplate(BaseDocTemplate):
    """Dieses Template definiert das Dokument Online-Handlungshilfe"""

    def __init__(self, filename, **kw):
        frame1 = Frame(1 * cm, 1 * cm, 27 * cm, 18.5 * cm, id='F1', showBoundary=True)
        self.allowSplitting = 0
        apply(BaseDocTemplate.__init__, (self, filename), kw)
        self.addPageTemplates(PageTemplate('normal', [frame1]))

#Definition der Druck-Funktion
def createpdf(context, tmpfile, ma, gb, sb, langvar='de'):
    """
    Schreibt eine PDF-Datei
    """

    story = []

    langvar='de'
    styleSheet = getSampleStyleSheet()
    styleSheet = getSampleStyleSheet()
    h1 = styleSheet['Heading1']
    h2 = styleSheet['Heading2']
    h3 = styleSheet['Heading3']
    code = styleSheet['Code']
    bt = styleSheet['BodyText']
    
	
    #Timestamp
    timestamp=strftime("%d%m%Y%H%M%S",gmtime()) #Ermitteln der aktuellen Uhrzeit und Formatierung eines Strings mit Zeitstempel

    #Variablen 
    datum = strftime("%d.%m.%Y",gmtime())


    #BGETEM Header
    story.append(Paragraph(translate(_(u"DGUV Vorschrift 2 - Online Handlungshilfe"), target_language=langvar), h1))        
    story.append(Spacer(0 * cm, 0.5 * cm)) # Was wird davon in den Ueberschriftsformaten bereits gesteuert?
    story.append(Paragraph(translate(_(u"(Ermittlung des Umfangs der betriebsärztlichen und sicherheitstechnischen"), target_language=langvar), h2))
    story.append(Spacer(0 * cm, 0.5 * cm))
    story.append(Paragraph(translate(_(u"Regelbetreuung in Betrieben mit mehr als 10 Beschäftigten)"), target_language=langvar), h2))
   
    story.append(Spacer(0 * cm, 1 * cm)) 
    story.append(Paragraph(translate(_(u'gedruckt, am: '), target_language=langvar) + datum, h2))

    #c.setFont(schriftart,11)
    #c.drawString(2.5*cm,13.9*cm, translate(_(u'Anzahl der Beschäftigten im Betrieb (Ihre Angaben):'), target_language=langvar) + ' ' + str(ma.get('mitarbeiter', '')))

    #c.setFont(schriftartfett,11)
    #c.drawString(2.5*cm,12.8*cm, translate(_(u'Ergebnisse für Ihren Betrieb'), target_language=langvar))

    #Stylesheet fuer Paragraphen in den Tabellen????
    stylesheet = getSampleStyleSheet()
    stylesheet.add(ParagraphStyle(name='normal', fontName='Helvetica', fontSize=9, borderPadding = (5,3,3,5)))
    stylesheet.add(ParagraphStyle(name='valuer', fontName='Helvetica-Bold', fontSize=9, borderPadding = (5,3,3,5), alignment=_r))
    stylesheet.add(ParagraphStyle(name='value', fontName='Helvetica-Bold', fontSize=9, borderPadding = (5,3,3,5)))
    style_norm = stylesheet['normal']
    style_valuer= stylesheet['valuer']
    style_value = stylesheet['value']
    

    #Daten zur Grundbetreuung
    story.append(Spacer(0 * cm, 1 * cm))
    story.append(Paragraph(translate(_(u'1.Grundbetreuung'), target_language=langvar), h2))
  
    if gb.has_key('wzcodenr'):
        tabledata = [[Paragraph(translate(_(u'Ihr WZ-Kode:'), target_language=langvar), style_norm), Paragraph(str(gb.get('wzcodenr', '')), style_value)],
                     [Paragraph(translate(_(u'Betriebsart:'), target_language=langvar), style_norm), Paragraph(str(gb.get('wzcodetext', '')), style_value)],
                     [Paragraph(translate(_(u'Betreuungsgruppe:'), target_language=langvar), style_norm), Paragraph(str(gb.get('bgruppe', '')), style_value)],
                     [Paragraph(translate(_(u'Einsatzzeitensumme für Betriebsarzt und Fachkraft für Arbeitssicherheit:'), target_language=langvar), style_norm), 
                         Paragraph(str(gb.get('gb_data', '')) + translate(_(u' Stunden pro Jahr'), target_language=langvar), style_value)],
                     [Paragraph(translate(_(u'Mindestanteil für Betriebsarzt bzw. Fachkraft für Arbeitssicherheit:'), target_language=langvar), style_norm),
                         Paragraph(str(gb.get('min', '')) + translate(_(u' Stunden pro Jahr'), target_language=langvar), style_value)]
                    ]
        
        colWidths = (9*cm, 8*cm)
        gbt = Table(tabledata, repeatRows=0, colWidths=colWidths, style=[('GRID',(0,0),(-1,-1),1, grey),])
        story.append(gbt)
    
    else:
    	story.append(Paragraph(translate(_(u'Das Modul Grundbetreuung wurde nicht von Ihnen bearbeitet.'), target_language=langvar), bt))

    fragen = formatFragen(context)
    aufgaben = formatAufgaben(context)

    story.append(Paragraph(translate(_(u'2. Betriebsspezifische Betreuung'), target_language=langvar), h2))
    story.append(Paragraph(translate(_(u'Relevante Aufgabenfelder für Ihren Betrieb und geschätzter Betreuungsumfang'), target_language=langvar), h2))
    story.append(Paragraph(translate(_(u'(Summe für Betriebsarzt und Fachkraft für Arbeitssicherheit)'), target_language=langvar), h2))

    #c.drawString(2.5*cm, 17.2*cm, u'Hinweis: je relevantes Aufgabenfeld wird ein Zeitbedarf von mindestens einer Stunde pro Jahr, für die betriebsspezifische Betreuung insgesamt (ohne')
    #c.drawString(2.5*cm, 16.7*cm, u'arbeitsmedizinische Vorsorge) ein Zeitbedarf von mindestens zwei Stunden pro Jahr angesetzt.')

    valuecols = len(sb.get('sbvalues'))

    colWidths = [6*cm,]
    for i in valuecols:
        colWidths.append(4*cm)
    colWidths.append(2*cm)

    bstable = []
    tableheader = [Paragraph(translate(_(u'Aufgabenfelder'), target_language=langvar), style_value),]
    for i in sb.get('sbvalues'):
        tableheader.append(Paragraph(fragen.get(i).get('title').decode('utf-8')),style_value) 
    tableheader.append(Paragraph(translate(_(u'Stunden pro Jahr'), target_language=langvar), style_value))
    bstable.append(tableheader)

    for i in sb.get('steps'):
        zeile = []
        entry = "%s %s" % (i, aufgaben.get(i).decode('utf-8'))
        zeile.append(entry)
        for k in sb.get('sbvalues', []):
            if k in sb['stepdata'][i]['valuedata']:
                auswahl_eintrag = sb['stepdata'][i]['data'][k]
                if fragen[k]['fieldtype'] == 'choice':
                    entry = fragen[k]['optionen'][auswahl_eintrag].decode('utf-8')
                    zeile.append(entry)
                else:
                    zeile.append(auswahl_eintrag)
            else:
                zeile.append()
        if sb['stepdata'][i]['alt']:
            entry = sb['stepdata'][i]['alt'].decode('utf-8')
            zeile.append(entry)
        else:
            value = sb['stepdata'][i]['stepvalue']
            zeile.append(value)
        bstable.append(zeile)

    ergebnis = [Paragraph(translate(_(u'Summe der relevanten Aufgabenfelder'), target_language=langvar), style_value),]
    for i in valuecols: 
        ergebnis.append(Paragraph(u'', style_value))
    ergebnis.append(Paragraph(str(sb.get("sbsum")), style_valuer))

    bstable.append(ergebnis)

    #sbtable = Table(tabledata, repeatRows=0, colWidths=colWidths, style=[('GRID',(0,0), (-1,-1), 1, grey),
    #                                                                             ('SPAN',(0,-1),(4,-1)),])

    sbtable = Table(tabledata, repeatRows=0, colWidths=colWidths, style=[('GRID',(0,0), (-1,-1), 1, grey),])
    
    story.append(sbtable)

    path = '/tmp/handlungshilfe.pdf'
    path = tmpfile
    doc = HHTemplate(path, pagesize=landscape(A4))
    doc.build(story)
