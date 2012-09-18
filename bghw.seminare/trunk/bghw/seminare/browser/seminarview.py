# -*- coding:utf-8 -*-
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


    def getTableData(self):
        """
        returns the table data
        """
        fo = self.context.datefile
        wb = open_workbook(file_contents = str(fo))
        ts = wb.sheet_by_name('termine')
        try:
            plzs = wb.sheet_by_name('plz')
        except:
            plzs = None

        postleitzahlen = []
        if plzs:
            for i in range(plzs.nrows):
                data = {}
                if i > 0:
                    data['vonPLZ'] = str(int(plzs.cell(i, 0).value)).zfill(5)
                    data['bisPLZ'] = str(int(plzs.cell(i, 1).value)).zfill(5)
                    data['sort'] = locations[int(plzs.cell(i, 2).value)]
                    postleitzahlen.append(data)
        
        termine = []
        for i in range(ts.nrows):
            data = {}
            if i > 0: #Ignoriert die Kopfzeile des Excel-Sheets

                data['sort'] = locations[int(ts.cell(i, 0).value)]
                data['stype'] = ts.cell(i, 1).value

                #Die folgenden Zeilen formatieren Datum und Uhrzeit des Seminarbeginns
                parseDate = xldate_as_tuple(ts.cell(i, 2).value, wb.datemode)
                if ts.cell(i, 4).value and not isinstance(ts.cell(i, 4).value, unicode):
                    parseTime = xldate_as_tuple(ts.cell(i, 4).value, wb.datemode)
                elif ts.cell(i, 4).value and isinstance(ts.cell(i, 4).value, unicode):
                    parseTime = (0,0,0,int(ts.cell(i, 4).value.split(':')[0]), int(ts.cell(i, 4).value.split(':')[1]), 0)
                else:
                    parseTime = (0,0,0,12,0,0)
                data['von'] = "%s.%s.%s %s:%s" %(parseDate[2], parseDate[1], parseDate[0], parseTime[3], str(parseTime[4]).zfill(2))
                parseDate = xldate_as_tuple(ts.cell(i, 3).value, wb.datemode)
                if ts.cell(i, 5).value and not isinstance(ts.cell(i, 5).value, str):
                    parseTime = xldate_as_tuple(ts.cell(i, 5).value, wb.datemode)
                elif ts.cell(i, 5).value and isinstance(ts.cell(i, 5).value, str):
                    parseTime = (0,0,0,int(ts.cell(i, 5).value.split(':')[0]), int(ts.cell(i, 5).value.split(':')[1]), 0)
                else:
                    parseTime = (0,0,0,12,0,0)
                data['bis'] = "%s.%s.%s %s:%s" %(parseDate[2], parseDate[1], parseDate[0], parseTime[3], str(parseTime[4]).zfill(2))

                data['thema'] = ts.cell(i, 6).value

                data['folge1'] = '' 
                if ts.cell(i, 7).value:
                    parseVon = xldate_as_tuple(ts.cell(i, 7).value, wb.datemode)
                    parseTo = xldate_as_tuple(ts.cell(i, 8).value, wb.datemode)
                    data['folge1'] = '%s.%s.%s-%s.%s.%s' %(parseVon[2], parseVon[1], parseVon[0],
                                                           parseTo[2], parseTo[1], parseTo[0],)
                data['folge2'] = ''
                if ts.cell(i, 11).value:
                    parseVon = xldate_as_tuple(ts.cell(i, 11).value, wb.datemode)
                    parseTo = xldate_as_tuple(ts.cell(i, 12).value, wb.datemode)
                    data['folge1'] = '%s.%s.%s-%s.%s.%s' %(parseVon[2], parseVon[1], parseVon[0],
                                                                   parseTo[2], parseTo[1], parseTo[0],)
                data['nacht'] = False
                data['ausgebucht'] = False
                if ts.cell(i, 15).value:
                    data['nacht'] = True
                if ts.cell(i, 16).value:
                    data['ausgebucht'] = True
                termine.append(data)

        print postleitzahlen
        print termine

