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
from database_setup import mitik, mitik2, users
from sqlalchemy.sql import select, and_
from zeam.form.base import NO_VALUE, DictDataManager


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

    def formatHU(self, result):
        az = ""
        if result.az != "00":
            az = "-%s" % result.az
        return "%s%s" %(result.login, az)

    @action(u'Suchen')
    def handel_search(self):
        v = False
        data, errors = self.extractData()
        if errors:
            return errors
        sql = select([mitik, mitik2, users],
            and_(mitik.c.iknr==mitik2.c.trgiknr, 
                 mitik2.c.trgrcd==users.c.oid))
        if data.get('mnr') != NO_VALUE:
            sql = sql.where(mitik2.c.trgmnr == data.get('mnr')) 
            v = True 
        if data.get('name1') != NO_VALUE:
            sql = sql.where(mitik.c.iknam1.like(data.get('name1')+'%')) 
            v = True 
        if data.get('strasse') != NO_VALUE:
            sql = sql.where(mitik.c.ikstr.like(data.get('strasse')+'%')) 
            v = True 
        if data.get('ort') != NO_VALUE:
            sql = sql.where(mitik.c.ikhort.like(data.get('ort')+'%')) 
            v = True 
        if data.get('login') != NO_VALUE:
            sql = sql.where(users.c.login.like(data.get('login')+'%')) 
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

    ignoreContent = False

    fields = Fields(IChangePassword)
    fields['login'].mode = "hiddendisplay"
    fields['oid'].mode = "hiddendisplay"
    fields['az'].mode = "hiddendisplay"

    obj = None
    oid = None

    def update(self):
        self.oid = self.request.get('oid')
        self.az = self.request.get('az')
        if self.oid:
            sql = select([mitik, mitik2, users],
                and_(mitik.c.iknr==mitik2.c.trgiknr,
                     mitik2.c.trgrcd==self.oid,
                     users.c.az == self.az,
                     mitik2.c.trgrcd==users.c.oid))
            session = Session()
            self.obj = session.execute(sql).fetchone()

    def getContentData(self):
        return DictDataManager(dict(
            passwort = self.obj.passwort.strip(),
            email = self.obj.email.strip(),
            login = self.obj.login.strip(),
            az = self.obj.az.strip(),
            vname = self.obj.vname.strip(),
            nname = self.obj.nname.strip(),
            vwhl = self.obj.vwhl.strip(),
            tlnr = self.obj.tlnr.strip(),
            oid = self.obj.oid,
            merkmal = self.obj.merkmal.strip(),
            ))

    @action(u'Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            return 
        upd = users.update().where(and_(users.c.oid==data.get('oid'), users.c.az==data.get('az'))).values(
                passwort=data.get('passwort'), 
                vname=data.get('vname'), 
                nname=data.get('nname'), 
                vwhl=data.get('vwhl'), 
                tlnr=data.get('tlnr'), 
                email=data.get('email',)) 
        session = Session()
        print upd
        session.execute(upd)
        self.redirect(self.application_url())

    @action(u'Abbrechen')
    def handle_cancel(self):
        self.flash(u'Aktion abgebrochen')
        self.redirect(self.application_url())


class AsPdf(grok.View):
    grok.name('pdf')
    menu.menuitem('documentactions', icon="fanstatic/example/icons/pdf.png")

    def render(self):
        return "I Should BE A PDF"
