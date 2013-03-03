# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from uv.bsbetreuung import bsbetreuungMessageFactory as _

class FinalViewlet(ViewletBase):
    render = ViewPageTemplateFile('final.pt')

    @property
    def getSessionCookie(self):
        session = self.context.session_data_manager.getSessionData()
        return session

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def formatFragen(self):
        pcat = self.portal_catalog
        brains = pcat(portal_type = 'Fragestellung', review_state='published', show_inactive=True)
        fragen = {}
        for i in brains:
            mydict = {}
            frage = i.getObject()
            mydict['title'] = frage.title
            mydict['fieldtype'] = frage.fieldtype
            optionen = {}
            for j in frage.optionen:
                option = j.split('|')
                optionen[option[0]] = option[1]
            mydict['optionen'] = optionen
            fragen[frage.id] = mydict
        return fragen    
    
    @property
    def formatAufgaben(self):
        pcat = self.portal_catalog
        brains = pcat(portal_type = 'Aufgabe', review_state='published', show_inactive=True)
        aufgaben = {}
        for i in brains:
            aufgabe = i.getObject()
            aufgaben[aufgabe.nummer] = aufgabe.title
        return aufgaben    

    def genTable(self, sb):
        fragen = self.formatFragen
        aufgaben = self.formatAufgaben
        table = '<table class="grid listing"><tr><th>%s</th>' % _(u'Aufgabenfelder')
        for i in sb.get('sbvalues'):
            table += "<th>%s</th>" % fragen.get(i).get('title')
        table += "<th>%s</th></tr>" % _(u'Stunden pro Jahr')
        for i in sb.get('steps'):
            table += "<tr><td>%s</td>" % i + ' ' + aufgaben.get(i)
            for k in sb.get('sbvalues'):
                if k in sb['stepdata'][i]['valuedata']:
                    auswahl_eintrag = sb['stepdata'][i]['data'][k]
                    print fragen
                    print i, k, auswahl_eintrag
                    if fragen[k]['fieldtype'] == 'choice':
                        table += "<td>%s</td>" % fragen[k]['optionen'][auswahl_eintrag]
                    else:
                        table += "<td>%s</td>" % auswahl_eintrag
                else:
                    table += "<td></td>"
            if sb['stepdata'][i]['alt']:       
                table += "<th>%s</th></tr>" % sb['stepdata'][i]['alt']
            else:    
                table += "<th>%s</th></tr>" % sb['stepdata'][i]['stepvalue']    
        colspan = 1 + len(sb.get('sbvalues'))
        abschluss = _(u"Geschätzter Betreuungsaufwand für die betriebsspezifische Betreuung (ohne arbeitsmedizinische Vorsorge)")
        table += '<tr><th colspan="%s">%s</td><td>%s</td></tr>' % (colspan, abschluss, sb.get("sbsum"))
        table += "</table>"
        return table


    def update(self):
        session = self.getSessionCookie
        self.ma = session.get('start')
        self.gb = session.get('gb')
        sb = session.get('sb')
        self.table = self.genTable(sb)

