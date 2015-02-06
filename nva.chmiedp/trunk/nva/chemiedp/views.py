# -*- coding:utf-8 -*-
from Acquisition import aq_inner, aq_parent
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from zope.interface import Interface
from uvc.api import api
from nva.chemiedp.herstellerordner import IHerstellerOrdner
from nva.chemiedp.produktordner import IProduktOrdner
from nva.chemiedp.hersteller import IHersteller
from nva.chemiedp.reinigungsmittelmanuell import IReinigungsmittelManuell
from nva.chemiedp.reinigungsmitteletiketten import IReinigungsmittelEtiketten
from nva.chemiedp.druckbestaeubungspuder import IDruckbestaeubungspuder
from nva.chemiedp.vocabularies import anwendungsgebieteVocab, zweckVocab
from nva.chemiedp.vocabularies import klasse as klasseVocab
from nva.chemiedp.vocabularies import ausgangsmaterial as materialVocab

api.templatedir('viewtemplates')


def back_references(source_object, attribute_name):
    """ Return back references from source object on specified attribute_name """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                            dict(to_id=intids.getId(aq_inner(source_object)),
                                 from_attribute=attribute_name)
                            ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result

def createRefsSnippet(objectlist):
    """Return a Html-Snippet with an unnumbered list"""
    snippet = '<ul>'
    for i in objectlist:
        row = '<li><a href="%s">%s</a></li>' %(i.absolute_url(),i.title)
        snippet += row
    snippet += '</ul>'
    return snippet


def createPullDownSnippet(objectlist):
    chemikalie = {u'nva.chemiedp.reinigungsmittelmanuell':u'Sonderreiniger',
                  u'nva.chemiedp.reinigungsmitteletiketten':u'Etikettenreiniger',
                  u'nva.chemiedp.druckbestaeubungspuder':u'Druckbestäubungspuder'}
    objlist_ordered = {u'Sonderreiniger':[], u'Etikettenreiniger':[], u'Druckbestäubungspuder':[]}
    for i in objectlist:
        objlist_ordered[chemikalie.get(i.portal_type)].append(i)

    #Clearing, wenn Hersteller nicht über das gesamte Produktportfolio verfügen 
    if not objlist_ordered['Sonderreiniger']:
        del objlist_ordered[u'Sonderreiniger']
    if not objlist_ordered[u'Etikettenreiniger']:
        del objlist_ordered[u'Etikettenreiniger']
    if not objlist_ordered[u'Druckbestäubungspuder']:
        del objlist_ordered[u'Druckbestäubungspuder']
    ##########################################################

    snippet = '<ul class="dropdown-menu dropdown-menu-right" role="menu" aria-labelledby="dropdownMenu2">'
    for i in objlist_ordered:
        snippet += '<li role="presentation" class="dropdown-header">%s</li>\r\n' % i
        for j in objlist_ordered[i]:
            snippet += '<li role="presentation"><a tabindex="-1" role="menuitem" href="%s">%s</a></li>\r\n' %(j.absolute_url(), j.title)
        snippet += '<li role="presentation" class="divider"></li>'
    snippet += '</ul>'
    return snippet

def createAddressSnippet(anschrift1, anschrift2, anschrift3, land, telefon, telefax):
    snippet = u'<div class="adresse"><p>%s</p>' %anschrift1
    if anschrift2:
        snippet += '<p>%s</p>' %anschrift2
    if anschrift3:
        snippet += '<p>%s</p>' %anschrift3
    snippet += '<p>%s</p>' %land
    snippet += '</div>'
    snippet += '<div class="contact"><table class="table table-striped">'
    snippet += '<tr><th>Telefon</th><td data-title="Telefon">%s</td></tr>' %telefon
    if telefax:
        snippet += '<tr><th>Telefax</th><td data-title="Telefax">%s</td></tr>' %telefax
    snippet += '</div>'
    return snippet

class HerstellerView(api.Page):
    api.context(IHersteller)

class SonderreinigerView(api.Page):
    api.context(IReinigungsmittelManuell)

    def update(self):
        self.parenturl = self.context.aq_inner.aq_parent.absolute_url()

class HerstellerOrdnerView(api.Page):
    api.context(IHerstellerOrdner)
    
    def update(self):
        fc = self.context.getFolderContents()
        objlist=[]
        for i in fc:
            entry={}
            obj=i.getObject()
            entry["backrefs"] = createPullDownSnippet(back_references(obj, 'hersteller'))
            entry["title"]=obj.title
            entry["anschrift"] = createAddressSnippet(obj.anschrift1, obj.anschrift2, obj.anschrift3, obj.land, obj.telefon, obj.telefax)
            entry["anschrift2"]=obj.anschrift2
            entry["anschrift3"]=obj.anschrift3
            entry["url"]=obj.absolute_url()
            entry["homepage"]=obj.homepage
            entry["email"]=obj.email
            if entry["backrefs"]:
                objlist.append(entry)
        self.objlist= objlist

class SonderreinigerOrdnerView(api.Page):
    api.context(IProduktOrdner)

    def update(self):
        fc = self.context.getFolderContents()
        herstellerdict = {}
        objdict = {}
        query_anwendungsgebiet = self.request.get('anwendungsgebiet', '')
        query_flammpunkt = self.request.get('flammpunkt', '')
        for i in fc:
            entry = {}
            obj = i.getObject()
            if not objdict.has_key(obj.hersteller.to_object.id):
                objdict[obj.hersteller.to_object.id] = []
                herstellerdict[obj.hersteller.to_object.id] = obj.hersteller.to_object.title
            entry['title'] = obj.title
            entry['url'] = obj.absolute_url()
            anwendungsgebiete = [anwendungsgebieteVocab.getTerm(i).title for i in obj.anwendungsgebiete]
            entry['anwendungsgebiete'] = ', '.join(anwendungsgebiete)
            relsign = ''
            if obj.wertebereich:
                relsign = '>'
            flammpunkt = u'nicht anwendbar'
            if obj.flammpunkt:
                flammpunkt = unicode(obj.flammpunkt)
                if obj.wertebereich:
                    flammpunkt = u'>' + flammpunkt
            entry['flammpunkt'] = flammpunkt
            emissionsgeprueft = 'nein'
            if obj.emissionsgeprueft:
                emissionsgeprueft = 'ja'
            entry['emissionsgeprueft'] = emissionsgeprueft
            if query_flammpunkt and obj.flammpunkt:
                if query_flammpunkt == '40-60':
                    if 40 <= obj.flammpunkt <= 60 and not obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                    if 40 < obj.flammpunkt <= 55 and obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                if query_flammpunkt == '61-99':
                    if 61 <= obj.flammpunkt <= 99 and not obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                    if 61 < obj.flammpunkt <= 95 and obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                if query_flammpunkt == '100':
                    if obj.flammpunkt >= 100:
                        objdict[obj.hersteller.to_object.id].append(entry)
                    if obj.flammpunkt >95 and obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
            elif query_flammpunkt and not obj.flammpunkt:
                if query_flammpunkt == 'na':
                        objdict[obj.hersteller.to_object.id].append(entry)
            elif query_anwendungsgebiet:
                if query_anwendungsgebiet in obj.anwendungsgebiete:
                    objdict[obj.hersteller.to_object.id].append(entry)
            else:
                objdict[obj.hersteller.to_object.id].append(entry)
        self.objects = objdict
        myhersteller = objdict.keys()
        myhersteller.sort()
        self.myhersteller = myhersteller
        self.hersteller = herstellerdict
        self.url = self.context.absolute_url()
        self.alle = 'dropdown'
        self.flammpunkt = 'dropdown'
        self.anwendungsgebiet = 'dropdown'
        self.collapse = 'collapse'
        if self.request.get('flammpunkt'):
            self.flammpunkt = 'dropdown active'
            self.collapse = 'collapse in'
        elif self.request.get('anwendungsgebiet'):
            self.anwendungsgebiet = 'dropdown active'
            self.collapse = 'collapse in'
        else:
            self.alle = 'dropdown active'
            self.collapse = 'collapse'  


def splitEinstufungen(einstufungen):
    oldpicts = []
    picts = []
    words = []
    if 'xi-reizend' in einstufungen:
        oldpicts.append('reizend_xi.png')
    if 'xn-gesundheitsschaedlich' in einstufungen:
        oldpicts.append('gesundheitsschaedlich_xn.png')
    if 'piktogramm-achtung' in einstufungen:
        picts.append('piktogramm_achtung.png')
    if 'piktogramm-aetzend' in einstufungen:
        picts.append('piktogramm_aetzend.png')
    if 'piktogramm-entflammbar' in einstufungen:
        picts.append('piktogramm_entflammbar.png')
    if 'signalwort-achtung' in einstufungen:
        words.append(u'Achtung')
    if 'signalwort-gefahr' in einstufungen:
        words.append(u'Gefahr')
    return {'oldpicts':oldpicts, 'picts':picts, 'words': ', '.join(words)}        

class EtikettenOrdnerView(api.Page):
    api.context(IProduktOrdner)

    def update(self):
        fc = self.context.getFolderContents()
        herstellerdict = {}
        objdict = {}
        query_verwendungszweck = self.request.get('verwendungszweck', '')
        query_flammpunkt = self.request.get('flammpunkt', '')
        for i in fc:
            entry = {}
            obj = i.getObject()
            if not objdict.has_key(obj.hersteller.to_object.id):
                objdict[obj.hersteller.to_object.id] = []
                herstellerdict[obj.hersteller.to_object.id] = obj.hersteller.to_object.title
            entry['title'] = obj.title
            entry['url'] = obj.absolute_url()
            entry['einstufungen'] = splitEinstufungen(obj.einstufung)
            entry['saetze'] = ''
            if obj.saetze:
                entry['saetze'] = ', '.join(obj.saetze)
            verwendungszwecke = [zweckVocab.getTerm(i).title for i in obj.verwendungszweck]
            entry['verwendungszwecke'] = ', '.join(verwendungszwecke)
            relsign = ''
            if obj.wertebereich:
                relsign = '>'
            flammpunkt = u'nicht anwendbar'
            if obj.flammpunkt:
                flammpunkt = unicode(obj.flammpunkt)
                if obj.wertebereich:
                    flammpunkt = u'>' + flammpunkt
            entry['flammpunkt'] = flammpunkt
            emissionsgeprueft = 'nein'
            if obj.emissionsgeprueft:
                emissionsgeprueft = 'ja'
            entry['emissionsgeprueft'] = emissionsgeprueft
            if query_flammpunkt and obj.flammpunkt:
                if query_flammpunkt == '40-60':
                    if 40 <= obj.flammpunkt <= 60 and not obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                    if 40 < obj.flammpunkt <= 55 and obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                if query_flammpunkt == '61-99':
                    if 61 <= obj.flammpunkt <= 99 and not obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                    if 61 < obj.flammpunkt <= 95 and obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
                if query_flammpunkt == '100':
                    if obj.flammpunkt >= 100:
                        objdict[obj.hersteller.to_object.id].append(entry)
                    if obj.flammpunkt >95 and obj.wertebereich:
                        objdict[obj.hersteller.to_object.id].append(entry)
            elif query_flammpunkt and not obj.flammpunkt:
                if query_flammpunkt == 'na':
                        objdict[obj.hersteller.to_object.id].append(entry)
            elif query_verwendungszweck:
                if query_verwendungszweck in obj.verwendungszweck:
                    objdict[obj.hersteller.to_object.id].append(entry)
            else:
                objdict[obj.hersteller.to_object.id].append(entry)
        self.objects = objdict
        myhersteller = objdict.keys()
        myhersteller.sort()
        self.myhersteller = myhersteller
        self.hersteller = herstellerdict
        self.url = self.context.absolute_url()
        self.alle = 'dropdown'
        self.flammpunkt = 'dropdown'
        self.verwendungszweck = 'dropdown'
        self.collapse = 'collapse'
        if self.request.get('flammpunkt'):
            self.flammpunkt = 'dropdown active'
            self.collapse = 'collapse in'
        elif self.request.get('verwendungszweck'):
            self.verwendungszweck = 'dropdown active'
            self.collapse = 'collapse in'
        else:
            self.alle = 'dropdown active'
            self.collapse = 'collapse'  

class EtikettenreinigerView(api.Page):
    api.context(IReinigungsmittelEtiketten)

    def update(self):
        self.parenturl = self.context.aq_inner.aq_parent.absolute_url()
        self.einstufungen = splitEinstufungen(self.context.einstufung)
        self.saetze = ''
        if self.context.saetze:
            self.saetze = ', '.join(self.context.saetze)

class PuderOrdnerView(api.Page):
    api.context(IProduktOrdner)

    def update(self):
        fc = self.context.getFolderContents()
        herstellerdict = {}
        objdict = {}
        #import pdb;pdb.set_trace()
        query_produktklasse = self.request.get('produktklasse', '')
        query_material = self.request.get('material', '')
        for i in fc:
            entry = {}
            obj = i.getObject()
            if not objdict.has_key(obj.hersteller.to_object.id):
                objdict[obj.hersteller.to_object.id] = []
                herstellerdict[obj.hersteller.to_object.id] = obj.hersteller.to_object.title
            entry['title'] = obj.title
            entry['url'] = obj.absolute_url()
            entry['produktklasse'] = klasseVocab.getTerm(obj.produktklasse).title
            entry['material'] = materialVocab.getTerm(obj.ausgangsmaterial).title
            entry['medianwert'] = obj.medianwert
            entry['volumenanteil'] = obj.volumenanteil
            entry['maschinen'] = ''
            if obj.maschinen:
                entry['maschinen'] = ', '.join(obj.maschinen)
            #emissionsgeprueft = 'nein'
            #if obj.emissionsgeprueft:
            #    emissionsgeprueft = 'ja'
            #entry['emissionsgeprueft'] = emissionsgeprueft
            if query_produktklasse:
                if query_produktklasse == obj.produktklasse:
                    objdict[obj.hersteller.to_object.id].append(entry)
            elif query_material:
                if query_material == obj.ausgangsmaterial:
                    objdict[obj.hersteller.to_object.id].append(entry)
            else:
                objdict[obj.hersteller.to_object.id].append(entry)
        self.objects = objdict
        myhersteller = objdict.keys()
        myhersteller.sort()
        self.myhersteller = myhersteller
        self.hersteller = herstellerdict
        self.url = self.context.absolute_url()
        self.alle = 'dropdown'
        self.produktklasse = 'dropdown'
        self.material = 'dropdown'
        self.collapse = 'collapse'
        if self.request.get('produktklasse'):
            self.produktklasse = 'dropdown active'
            self.collapse = 'collapse in'
        elif self.request.get('material'):
            self.material = 'dropdown active'
            self.collapse = 'collapse in'
        else:
            self.alle = 'dropdown active'
            self.collapse = 'collapse'  

class PuderView(api.Page):
    api.context(IDruckbestaeubungspuder)

    def update(self):
        self.parenturl = self.context.aq_inner.aq_parent.absolute_url()
