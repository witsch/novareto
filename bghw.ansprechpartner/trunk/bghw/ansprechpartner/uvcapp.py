# -*- coding: utf-8 -*-
from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface
from bghw.ansprechpartner.interfaces import IPlzOrtSuche
from bghw.ansprechpartner.excel_datenbasis import IExcelDatenbasis
from bghw.ansprechpartner.container_ansprechpartner import IContainerAnsprechpartner
from bghw.ansprechpartner.interfaces import IUVCAnsprechpartnersuche
from bghw.ansprechpartner.lib.tabreader import findTabByPlz, findTabByOrt, findRehaByPlzName
from plone.app.layout.viewlets.interfaces import IBelowContentBody
from zeam.form.base import Fields, action
from zeam.form.base.markers import NO_VALUE

grok.templatedir('uvcapp_templates')

class uvcapp_Fields(grok.View):
    grok.context(Interface)

class AnsprechpartnerSuche(uvcsite.Form):
    """Form fuer die Suche nach Postleitzahl und Ort."""
    grok.context(IContainerAnsprechpartner)
    fields = Fields(IPlzOrtSuche).omit('ort')

    def update(self):
        self.data = {}
        fc = self.context.getFolderContents()
        for i in fc:
            obj = i.getObject()
            abteilung = obj.abteilung
            filedata = obj.excelfile.data
            self.data[abteilung] = filedata

    @uvcsite.action('suchen')
    def handle_search(self):
        import pdb;pdb.set_trace()
        data, errors = self.extractData()
        if errors:
            return
        self.data['formdata'] = data

class PlzOrtSuche(uvcsite.Form):
    """Form fuer die Suche nach Postleitzahl und Ort."""
    grok.context(IExcelDatenbasis)
    fields = Fields(IPlzOrtSuche).omit('name')

    def update(self):
        abteilung = self.context.abteilung
        filedata = self.context.excelfile.data
        self.data = {}
        self.data[abteilung] = filedata

    @uvcsite.action('suchen')
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        self.data['formdata'] = data

class PlzNameSuche(uvcsite.Form):
    """Form fuer die Suche nach Postleitzahl und Ort."""
    grok.context(IExcelDatenbasis)
    fields = Fields(IPlzOrtSuche).omit('ort')

    def update(self):
        abteilung = self.context.abteilung
        filedata = self.context.excelfile.data
        self.data = {}
        self.data[abteilung] = filedata

    @uvcsite.action('suchen')
    def handle_search(self):
        data, errors = self.extractData()
        if errors:
            return
        self.data['formdata'] = data


class PraeventionViewlet(grok.Viewlet):
    grok.context(IUVCAnsprechpartnersuche)
    grok.viewletmanager(IBelowContentBody)

    def available(self):
        if not hasattr(self.view, 'data'):
            return False
        if self.view.data.has_key(u'Praevention'):
            return True
        return False

    def update(self):
        self.plzresults = {}
        self.ortresults = []
        self.retval = False
        if not hasattr(self.view, 'data'):
            return
        if self.view.data.get('formdata') and self.view.data.has_key(u'Praevention'):
            plz = self.view.data.get('formdata').get('plz')
            if plz and plz != NO_VALUE:
                self.plzresults = findTabByPlz(plz, self.view.data.get(u'Praevention'))
            ort = self.view.data.get('formdata').get('ort')
            if ort and ort != NO_VALUE:
                self.ortresults = findTabByOrt(ort, self.view.data.get(u'Praevention'))
            if self.plzresults or self.ortresults:
                self.retval = True

class RehaLeistungViewlet(grok.Viewlet):
    grok.context(IUVCAnsprechpartnersuche)
    grok.viewletmanager(IBelowContentBody)

    def available(self):
        if not hasattr(self.view, 'data'):
            return False
        if self.view.data.has_key(u'Reha/Leistung'):
            return True
        return False

    def update(self):
        if not hasattr(self.view, 'data'):
            return
        self.rd = None
        if self.view.data.get('formdata') and self.view.data.has_key(u'Reha/Leistung'):
            plz = self.view.data.get('formdata').get('plz')
            name = self.view.data.get('formdata').get('name')
            results = findRehaByPlzName(plz, name, self.view.data.get(u'Reha/Leistung'))
            self.rd = results.get('rd', '') 
            self.strnr = results.get('strnr', '') 
            self.plzort = "%s %s" % (results.get('plz', ''), results.get('ort', ''))
            self.tel = results.get('tel', '') 
            self.fax = results.get('fax', '') 
