# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grok
from megrok.layout import Page
from zeam.form.base import action
from dolmen.forms.base import ApplicationForm, Fields
from interfaces import IBenutzer, IChangePassword
from ukh_userhandling import resource
import megrok.pagetemplate as pt
from megrok.menu import menuitem
from uvc.layout.slots.menus import GlobalMenu
from megrok import menu
from z3c.saconfig import Session
from database_setup import mitik, mitik2
from sqlalchemy.sql import select, and_
from zeam.form.base import NO_VALUE


grok.templatedir('templates')


class Ukh_userhandling(grok.Application, grok.Container):
    pass


class Index(ApplicationForm):
    grok.title(u'Benutzer Verwaltung')
    label = u"Benutzerverwaltung"
    description = u"Hier können Sie Benuzterdaten verwalten"
    legend = u"Bitte die Suchkriterien eingeben"
    menu.menuitem('globalmenu')

    fields = Fields(IBenutzer)
    results = []

    @action(u'Suchen')
    def handel_search(self):
        v = False
        data, errors = self.extractData()
        if errors:
            return errors
        sql = select([mitik, mitik2],
            and_(mitik.c.iknr==mitik2.c.trgiknr))
        
        if data.get('name1') != NO_VALUE:
            sql = sql.where(mitik.c.iknam1 == data.get('name1')) 
            v = True 
        if data.get('plz') != NO_VALUE:
            sql = sql.where(mitik.c.ikhplz == data.get('plz')) 
            v = True 
        if data.get('ort') != NO_VALUE:
            sql = sql.where(mitik.c.ikhort == data.get('ort')) 
            v = True 
        if not v: 
            self.flash(u'Bitte geben Sie die Suchkriterien ein.') 
            return 
        session = Session()
        self.results = session.execute(sql).fetchall()


class ChangePassword(ApplicationForm):
    grok.name('changeuser')
    label = u"Benutzerverwaltung"
    description = u"Bitte geben Sie hier ihr neues Passwort ein."
    legend = "Bitte das neue Passwort eingeben."

    fields = Fields(IChangePassword)
    obj = None
    oid = None

    def update(self):
        self.oid = self.request.get('oid')
        if self.oid:
            sql = select([mitik, mitik2],
                and_(mitik.c.iknr==mitik2.c.trgiknr,
                     mitik2.c.trgrcd==self.oid))
            session = Session()
            self.obj = session.execute(sql).fetchone()

    @action(u'Speichern')
    def handle_save(self):
        pass

    @action(u'Abbrechen')
    def handle_cancel(self):
        self.flash(u'Aktion abgebrochen')
        self.redirect(self.application_url())


class AsPdf(grok.View):
    grok.name('pdf')
    menu.menuitem('documentactions', icon="fanstatic/example/icons/pdf.png")

    def render(self):
        return "I Should BE A PDF"
