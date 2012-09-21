# -*- coding:utf-8 -*-
from operator import itemgetter
from datetime import datetime
from zope.interface import implements, Interface
from xlrd import open_workbook, xldate_as_tuple

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from bghw.seminare.lib.locations import locations
from bghw.seminare import seminareMessageFactory as _

locations = locations()

class IseminarView(Interface):
    """
    seminar view interface
    """

    def test():
        """ test method"""


class seminarView(BrowserView):
    """
    seminar browser view
    """
    implements(IseminarView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}


    def openExcelWorkbook(self):
        """
        Oeffnet das Excel-Workbook und gibt die Sheets zurueck
        """
        fo = self.context.datefile
        wb = open_workbook(file_contents = str(fo))
        datemode = wb.datemode
        if not u'termine' in wb.sheet_names():
            print "Fehler: kein Sheet termine im Workbook"
        ts = wb.sheet_by_name('termine')
        plzs = None
        if u'plz' in wb.sheet_names():
            plzs = wb.sheet_by_name('plz')
        return {'plz':plzs, 'termine':ts, 'datemode':datemode}    


    def getOrteFromPlzRange(self, plz, plzs):
        """
        Gibt eine Liste mit den Schluesselziffern der Seminarorte zurueck
        """
        ortlist = []
        for i in range(plzs.nrows):
            if i > 0: #ignoriert die Kopfzeile
                if int(plzs.cell(i, 0).value) <= int(plz) <= int(plzs.cell(i, 1).value):
                    ortlist.append(int(plzs.cell(i, 2).value))
        return ortlist


    def getSeminarData(self, orte=False):
        """
        Gibt die Seminardaten für ausgewaehlte Orte zurueck
        """
        self.marker = False #Markiert das Vorhandensein von Folgeterminen
        workdict = self.openExcelWorkbook()
        ts = workdict.get('termine', None)
        datemode = workdict.get('datemode', 0)
        termine = []
        for i in range(ts.nrows):
            data = {}
            if i > 0: #Ignoriert die Kopfzeile des Excel-Sheets
                seminarort = int(ts.cell(i, 0).value)
                if not orte or seminarort in orte:

                    data['sort'] = locations[int(ts.cell(i, 0).value)]
                    data['stype'] = ts.cell(i, 1).value

                    #Die folgenden Zeilen formatieren Datum und Uhrzeit des Seminarbeginns
                    parseDate = xldate_as_tuple(ts.cell(i, 2).value, datemode)
                    if ts.cell(i, 4).value and not isinstance(ts.cell(i, 4).value, unicode):
                        parseTime = xldate_as_tuple(ts.cell(i, 4).value, datemode)
                    elif ts.cell(i, 4).value and isinstance(ts.cell(i, 4).value, unicode):
                        parseTime = (0,0,0,int(ts.cell(i, 4).value.split(':')[0]), int(ts.cell(i, 4).value.split(':')[1]), 0)
                    else:
                        parseTime = (0,0,0,12,0,0)
                    data['mysorter'] = datetime(*(parseDate[0], parseDate[1], parseDate[2], parseTime[3], parseTime[4])) 
                    data['von'] = data['mysorter'].strftime('%d.%m.%Y %H:%M') 
                    parseDate = xldate_as_tuple(ts.cell(i, 3).value, datemode)
                    if ts.cell(i, 5).value and not isinstance(ts.cell(i, 5).value, unicode):
                        parseTime = xldate_as_tuple(ts.cell(i, 5).value, datemode)
                    elif ts.cell(i, 5).value and isinstance(ts.cell(i, 5).value, unicode):
                        parseTime = (0,0,0,int(ts.cell(i, 5).value.split(':')[0]), int(ts.cell(i, 5).value.split(':')[1]), 0)
                    else:
                        parseTime = (0,0,0,12,0,0)
                    terminende = datetime(*(parseDate[0], parseDate[1], parseDate[2], parseTime[3], parseTime[4])) 
                    data['bis'] = terminende.strftime('%d.%m.%Y %H:%M')
                    data['thema'] = ts.cell(i, 6).value

                    data['folge1'] = '' 
                    if ts.cell(i, 7).value:
                        self.marker = True
                        parseVon = xldate_as_tuple(ts.cell(i, 7).value, datemode)
                        parseTo = xldate_as_tuple(ts.cell(i, 8).value, datemode)
                        data['folge1'] = '%s.%s.%s-%s.%s.%s' %(parseVon[2], parseVon[1], parseVon[0],
                                                               parseTo[2], parseTo[1], parseTo[0],)
                    data['folge2'] = ''
                    if ts.cell(i, 11).value:
                        parseVon = xldate_as_tuple(ts.cell(i, 11).value, datemode)
                        parseTo = xldate_as_tuple(ts.cell(i, 12).value, datemode)
                        data['folge1'] = '%s.%s.%s-%s.%s.%s' %(parseVon[2], parseVon[1], parseVon[0],
                                                               parseTo[2], parseTo[1], parseTo[0],)
                    data['nacht'] = False
                    data['ausgebucht'] = False
                    if ts.cell(i, 15).value:
                        data['nacht'] = True
                    if ts.cell(i, 16).value:
                        data['ausgebucht'] = True
                    aform = self.context.getAform()
                    formurl = self.context.absolute_url()
                    if aform:
                        formurl = aform.absolute_url()

                    data['url'] = "%s?titel=%s&ort=%s&von=%s&bis=%s&nacht=%s&gebucht=%s" %(formurl,
                                                                                           self.context.title.decode('utf-8'),
                                                                                           data['sort'],
                                                                                           data['von'],
                                                                                           data['bis'],
                                                                                           data['nacht'],
                                                                                           data['ausgebucht'],)

                    termine.append(data)
        newlist = sorted(termine, key=itemgetter('mysorter'))
        formdata = {'marker':self.marker, 'seminare':newlist}
        return formdata


    def getViewData(self):
        """
        Steuert die Anzeige des Views
        """
        plz = self.request.get('plz', None)
        plzs = self.openExcelWorkbook().get('plz', None)

        if plzs and not plz:
            #Datei verfuegt ueber ein plz-sheet aber die plz wurde nicht eingegeben
            formdata = {'seminare':[], 'marker':False, 'plzform':True}
        elif plzs and plz:
            #Datei verfuegt ueber ein plz-sheet und die plz wurde eingegeben
            try:
                int(plz)
                orte = self.getOrteFromPlzRange(plz, plzs)
                formdata = self.getSeminarData(orte)
                formdata['plzform'] = True
            except:
                formdata = {'seminare':[], 'marker':False, 'plzform':True}
        else:
            formdata = self.getSeminarData(orte=False)
            formdata['plzform'] = False
        return formdata
