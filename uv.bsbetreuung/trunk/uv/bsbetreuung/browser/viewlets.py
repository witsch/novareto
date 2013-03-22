# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from nva.bsbetreuung.lib.helpers import formatFragen, formatAufgaben, formatFloat
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

    def genTable(self, sb):
        if not sb:
            return ""
        fragen = formatFragen(self.context)
        aufgaben = formatAufgaben(self.context)
        table = '<table class="grid listing"><tr><th>%s</th>' % _(u'Aufgabenfelder')
        for i in sb.get('sbvalues'):
            entry = fragen.get(i).get('title').decode('utf-8')
            table += "<th>%s</th>" % entry
        table += "<th>%s</th></tr>" % _(u'Stunden pro Jahr')
        for i in sb.get('steps'):
            entry = aufgaben.get(i).decode('utf-8')
            table += "<tr><td>%s</td>" % i + ' ' + entry
            for k in sb.get('sbvalues', []):
                if k in sb['stepdata'][i]['valuedata']:
                    auswahl_eintrag = sb['stepdata'][i]['data'][k]
                    if fragen[k]['fieldtype'] == 'choice':
                        entry = fragen[k]['optionen'][auswahl_eintrag].decode('utf-8')
                        table += "<td>%s</td>" % entry
                    else:
                        table += "<td>%s</td>" % auswahl_eintrag
                elif k not in sb['stepdata'][i]['valuedata'] and sb['stepdata'][i]['alt']:
                    pass
                else:
                    table += "<td></td>"
            if sb['stepdata'][i]['alt']:
                colspan = 1 + len(sb.get('sbvalues'))
                entry = sb['stepdata'][i]['alt'].decode('utf-8')       
                table += '<td colspan="%s">%s</td></tr>' % (colspan, entry)
            else:
                value = formatFloat(sb['stepdata'][i]['stepvalue'])    
                table += '<th style="text-align:right;">%s</th></tr>' % value  
        colspan = 1 + len(sb.get('sbvalues'))
        summe = formatFloat(sb.get("sbsum"))
        abschluss = _(u"Geschätzter Betreuungsaufwand für die betriebsspezifische Betreuung (ohne arbeitsmedizinische Vorsorge)")
        table += '<tr><th colspan="%s">%s</td><th style="text-align:right;">%s</th></tr>' % (colspan, abschluss, summe)
        table += "</table>"
        return table


    def update(self):
        session = self.getSessionCookie
        self.ma = session.get('start', {})
        self.gb = session.get('gb', {})
        sb = session.get('sb', {})
        self.table = self.genTable(sb)

