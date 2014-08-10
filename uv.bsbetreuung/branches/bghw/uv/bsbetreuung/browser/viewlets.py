# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from nva.bsbetreuung.lib.helpers import formatFragen, formatAufgaben, formatFloat, getFragenInOrder
from nva.bsbetreuung.wizard import getSessionCookie as WizardSessionCookie
from uv.bsbetreuung import bsbetreuungMessageFactory as _
from collective.beaker.interfaces import ISession

class FinalViewlet(ViewletBase):
    render = ViewPageTemplateFile('final.pt')

    @property
    def getSessionCookie(self):
        cookie = WizardSessionCookie(self.context, self.request)
        session =  ISession(self.request)
        return (session, cookie)

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def genTable(self, sb):
        if not sb:
            return ""
        fragen = formatFragen(self.context)
        aufgaben = formatAufgaben(self.context)
        table = '<table class="table table striped"><tr><th>%s</th>' % _(u'Aufgabenfelder')
        sortedFragen = getFragenInOrder(self.context)

        print aufgaben

        sortedValues = [i.id for i in sortedFragen if i.id in sb.get('sbvalues')]

        for i in sortedFragen:
            if i.id in sb.get('sbvalues'):
                table += "<th>%s</th>" % i.title.decode('utf-8')
        table += "<th>%s</th></tr>" % _(u'Stunden pro Jahr')
        for i in sb.get('steps'):
            entry = aufgaben.get(i).decode('utf-8')
            tableentry = i + ' ' + entry
            table += "<tr><td>%s</td>" % tableentry
            for k in sortedValues:
                if k in sb['stepdata'][i.replace('.','_')]['valuedata']:
                    auswahl_eintrag = sb['stepdata'][i.replace('.','_')]['data'][k]
                    if fragen[k]['fieldtype'] == 'choice':
                        entry = fragen[k]['optionen'][auswahl_eintrag].decode('utf-8')
                        table += "<td>%s</td>" % entry
                    else:
                        table += "<td>%s</td>" % auswahl_eintrag
                elif k not in sb['stepdata'][i.replace('.','_')]['valuedata'] and sb['stepdata'][i.replace('.','_')]['alt']:
                    pass
                else:
                    table += "<td></td>"
            if sb['stepdata'][i.replace('.','_')]['alt']:
                colspan = 1 + len(sb.get('sbvalues'))
                entry = sb['stepdata'][i.replace('.','_')]['alt']
                table += '<td colspan="%s">%s</td></tr>' % (colspan, entry)
            else:
                value = formatFloat(sb['stepdata'][i.replace('.','_')]['stepvalue'])    
                table += '<th style="text-align:right;">%s</th></tr>' % value  
        colspan = 1 + len(sb.get('sbvalues'))
        summe = formatFloat(sb.get("sbsum"))
        abschluss = _(u"Geschätzter Betreuungsaufwand für die betriebsspezifische Betreuung (ohne arbeitsmedizinische Vorsorge)")
        table += '<tr><th colspan="%s">%s</td><th style="text-align:right;">%s</th></tr>' % (colspan, abschluss, summe)
        table += "</table>"
        return table


    def update(self):
        session = self.getSessionCookie[0]
        cookie = self.getSessionCookie[1]
        self.ma = session.get('start', {})
        self.gb = session.get('gb', {})
        self.table = self.genTable(cookie[0])

