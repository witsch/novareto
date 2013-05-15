# -*- coding: utf-8 -*-
# @author: Lars Walther

#Import der benoetigten Bibliotheken
from time import gmtime, strftime
from zope.i18n import translate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import grey

from reportlab.platypus.frames import Frame
from reportlab.platypus import Table
from reportlab.platypus.flowables import Flowable, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT as _r
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate

from nva.bsbetreuung.lib.helpers import formatFragen, formatAufgaben, formatFloat
from uv.bsbetreuung import bsbetreuungMessageFactory as _


class HHTemplate(BaseDocTemplate):
    """Dieses Template definiert das Dokument Online-Handlungshilfe"""

    def __init__(self, filename, **kw):
        frame1 = Frame(1 * cm, 1 * cm, 27 * cm, 18.5 * cm, id='F1', showBoundary=False)
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
    story.append(Paragraph(translate(_(u"(Ermittlung des Umfangs der betriebsärztlichen und sicherheitstechnischen"), target_language=langvar), h2))
    story.append(Paragraph(translate(_(u"Regelbetreuung in Betrieben mit mehr als 10 Beschäftigten)"), target_language=langvar), h2))
   
    story.append(Spacer(0 * cm, 0.5 * cm)) 
    story.append(Paragraph(translate(_(u'gedruckt, am: '), target_language=langvar) + datum, h3))

    #Stylesheet fuer Paragraphen in den Tabellen
    stylesheet = getSampleStyleSheet()
    stylesheet.add(ParagraphStyle(name='normal', fontName='Helvetica', fontSize=9, borderPadding = (5,3,3,5)))
    stylesheet.add(ParagraphStyle(name='valuer', fontName='Helvetica-Bold', fontSize=9, borderPadding = (5,3,3,5), alignment=_r))
    stylesheet.add(ParagraphStyle(name='value', fontName='Helvetica-Bold', fontSize=9, borderPadding = (5,3,3,5)))
    style_norm = stylesheet['normal']
    style_valuer= stylesheet['valuer']
    style_value = stylesheet['value']
    
    #Daten zur Grundbetreuung
    story.append(Spacer(0 * cm, 0.5 * cm))
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
    story.append(Paragraph(translate(_(u'Relevante Aufgabenfelder für Ihren Betrieb und geschätzter Betreuungsumfang'), target_language=langvar), bt))
    story.append(Paragraph(translate(_(u'(Summe für Betriebsarzt und Fachkraft für Arbeitssicherheit)'), target_language=langvar), bt))
    story.append(Spacer(0 * cm, 0.3 * cm))
 
    valuecols = len(sb.get('sbvalues'))

    colWidths = [6*cm,]
    for i in range(valuecols):
        colWidths.append(4*cm)
    colWidths.append(2*cm)

    bstable = []
    tableheader = [Paragraph(translate(_(u'Aufgabenfelder'), target_language=langvar), style_value),]
    for i in sb.get('sbvalues'):
        ueberschrift = fragen.get(i).get('title').decode('utf-8')
        tableheader.append(Paragraph(ueberschrift ,style_value))
    tableheader.append(Paragraph(translate(_(u'Stunden pro Jahr'), target_language=langvar), style_value))
    bstable.append(tableheader)

    fussnote = u'*'
    fussnoten = [] 
    for i in sb.get('steps'):
        zeile = []
        entry = "%s %s" % (i, aufgaben.get(i).decode('utf-8'))
        zeile.append(Paragraph(entry, style_value))
        for k in sb.get('sbvalues', []):
            if k in sb['stepdata'][i]['valuedata']:
                auswahl_eintrag = sb['stepdata'][i]['data'][k]
                if fragen[k]['fieldtype'] == 'choice':
                    entry = fragen[k]['optionen'][auswahl_eintrag].decode('utf-8')
                    zeile.append(Paragraph(entry, style_value))
                else:
                    zeile.append(Paragraph(auswahl_eintrag, style_value))
            else:
                zeile.append(Paragraph(u'', style_value))
        if sb['stepdata'][i]['alt']:
            entry = sb['stepdata'][i]['alt'].decode('utf-8')
            fussnoten.append((fussnote, entry))
            zeile.append(Paragraph(fussnote, style_value))
            fussnote += '*'
        else:
            value = formatFloat(sb['stepdata'][i]['stepvalue'])
            zeile.append(Paragraph(value, style_valuer))
        bstable.append(zeile)

    ergebnis = [Paragraph(translate(_(u'Summe der relevanten Aufgabenfelder'), target_language=langvar), style_value),]
    for i in range(valuecols): 
        ergebnis.append(Paragraph(u'', style_value))
    summe = formatFloat(sb.get("sbsum"))
    ergebnis.append(Paragraph(summe, style_valuer))

    bstable.append(ergebnis)

    #story.append(Table(tabledata, repeatRows=0, colWidths=colWidths, style=[('GRID',(0,0), (-1,-1), 1, grey),
    #                                                                        ('SPAN',(0,-1),(4,-1)),]))

    story.append(Table(bstable, repeatRows=0, colWidths=colWidths, style=[('GRID',(0,0), (-1,-1), 1, grey),]))

    for i in fussnoten:
        zeile = u"%s %s" % (i[0], i[1])
        story.append(Paragraph(zeile, style_norm))
    
    path = '/tmp/handlungshilfe.pdf'
    path = tmpfile
    doc = HHTemplate(path, pagesize=landscape(A4))
    doc.build(story)
