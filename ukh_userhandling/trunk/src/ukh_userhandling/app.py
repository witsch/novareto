# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grok
import megrok.pagetemplate as pt


from megrok.layout import Page
from zeam.form.base import action
from dolmen.forms.base import ApplicationForm, Fields, DISPLAY
from interfaces import IBenutzer, IChangePassword
from ukh_userhandling import resource
from ukh_userhandling.mail import send_mail
from uvc.layout.slots.menus import GlobalMenu
from megrok import menu
from z3c.saconfig import Session
from database_setup import users, z1ext1ab, z1ext1ac
from sqlalchemy.sql import select, and_
from zeam.form.base import NO_VALUE, DictDataManager
from zope.interface import Interface
from uvc.layout import MenuItem, IGlobalMenu


grok.templatedir('templates')

MT = u"""
Guten Tag,

Danke für Ihr Interesse am Mitgliederportal der Unfallkasse Hessen (UKH).

Ihr Login: %s
Ihr Kennwort: %s 

Bitte achten Sie bei der Eingabe auf die Groß-/Kleinschreibung.
Nach erfolgreicher Anmeldung können Sie ihr Passwort über den Menüpunkt "Meine Einstellungen" selbst ändern.

Ihre Fragen beantworten die Mitarbeiter unseres Servicetelefons sehr gern.
Wir freuen uns außerdem über Ihr Feedback zu unserem neuen Mitgliederservice!

Eine unfallfreie Zeit wünscht
Ihre Unfallkasse Hessen
"""



class Ukh_userhandling(grok.Application, grok.Container):
    pass


class BVMenuItem(MenuItem):
    grok.title(u'Benutzer Verwaltung')
    grok.context(Interface)
    grok.viewletmanager(IGlobalMenu)
    
    action = "index"



class Index(ApplicationForm):
    grok.title(u'Benutzer Verwaltung')
    label = u"Benutzerverwaltung"
    description = u"Hier können Sie Benuzterdaten verwalten"
    legend = u"Bitte die Suchkriterien eingeben"

    fields = Fields(IBenutzer)
    mitglieder = []
    einrichtungen = []

    def formatHU(self, result):
        az = ""
        if result.AZ != "00":
            az = "-%s" % result.AZ 
        return "%s%s" %(result.LOGIN, az)

    @action(u'Suchen')
    def handel_search(self):
        v = False
        data, errors = self.extractData()
        if errors:
            return errors
        sql = select([z1ext1ab])
            #and_(z1ext1ab.c.trgrcd==users.c.oid), use_labels=False)
        if data.get('mnr') != NO_VALUE:
            sql = sql.where(z1ext1ab.c.trgmnr == data.get('mnr')) 
            v = True 
        if data.get('name1') != NO_VALUE:
            sql = sql.where(z1extiab.c.iknam1.like(data.get('name1')+'%')) 
            v = True 
        if data.get('strasse') != NO_VALUE:
            sql = sql.where(z1ext1ab.c.ikstr.like(data.get('strasse')+'%')) 
            v = True 
        if data.get('ort') != NO_VALUE:
            sql = sql.where(z1ext1ab.c.ikhort.like(data.get('ort')+'%')) 
            v = True 
        if data.get('login') != NO_VALUE:
            sql = sql.where(z1ext1ab.c.login.like(data.get('login')+'%')) 
            v = True 
        if not v: 
            self.flash(u'Bitte geben Sie die Suchkriterien ein.') 
            return 
        session = Session()
        self.mitglieder = session.execute(sql).fetchall()
        sql = select([z1ext1ac])
            #and_(z1ext1ab.c.trgrcd==users.c.oid), use_labels=False)
        if data.get('mnr') != NO_VALUE:
            sql = sql.where(z1ext1ac.c.trgmnr == data.get('mnr')) 
            v = True 
        if data.get('name1') != NO_VALUE:
            sql = sql.where(z1extiac.c.iknam1.like(data.get('name1')+'%')) 
            v = True 
        if data.get('strasse') != NO_VALUE:
            sql = sql.where(z1ext1ac.c.ikstr.like(data.get('strasse')+'%')) 
            v = True 
        if data.get('ort') != NO_VALUE:
            sql = sql.where(z1ext1ac.c.ikhort.like(data.get('ort')+'%')) 
            v = True 
        if data.get('login') != NO_VALUE:
            sql = sql.where(z1ext1ac.c.login.like(data.get('login')+'%')) 
            v = True 
        if not v: 
            self.flash(u'Bitte geben Sie die Suchkriterien ein.') 
            return 
        session = Session()
        self.einrichtungen = session.execute(sql).fetchall()


class DisplayUser(ApplicationForm):
    label = "Benutzerverwaltung"
    description = u"Übersicht"
    legend = "Hier sehen Sie die Details zum Benutzer"
    mode = DISPLAY

    fields = Fields(IChangePassword)
    fields['oid'].mode = "hiddendisplay"
    fields['az'].mode = "hiddendisplay"
    fields['login'].mode = "hiddendisplay"
    fields['passwort'].mode = "hiddendisplay"
    fields['email'].mode = "hiddendisplay"
    ignoreContent = False
    obj = None
    
    def update(self):
        self.oid = self.request.get('oid')
        self.az = self.request.get('az')
        e = self.request.get('e', 'm')
        if self.oid and e == 'm':
            sql = select([z1ext1ab],
                and_(z1ext1ab.c.trgrcd==self.oid,
                     z1ext1ab.c.az == self.az,
                     ))
            session = Session()
            self.obj = session.execute(sql).fetchone()
        if self.oid and e == 'e':
            sql = select([z1ext1ac],
                and_(z1ext1ac.c.oid==self.oid,
                     z1ext1ac.c.az == self.az,
                     ))
            session = Session()
            self.obj = session.execute(sql).fetchone()

    def getContentData(self):
        if not self.obj:
            return DictDataManager({})
        return DictDataManager(dict(
            passwort = self.obj.passwort.strip(),
            email = self.obj.email.strip(),
            login = self.obj.login.strip(),
            az = self.obj.az.strip(),
            vname = self.obj.vname.strip(),
            funktion = self.obj.funktion,
            anr = self.obj.anr,
            titel = self.obj.titel,
            nname = self.obj.nname.strip(),
            vwhl = self.obj.vwhl.strip(),
            tlnr = self.obj.tlnr.strip(),
            oid = self.obj.oid,
            merkmal = self.obj.merkmal.strip(),
            ))
        
    @action(u'Senden des Passworts')
    def handle_send(self):
        data, errors = self.extractData()
        sender = "ukh@ukh.de"
        recipient = [data.get('email'), ]
        subject = "Neue Anmeldeinformationen für das Extranet"
        login = data.get('login')
        if data.get('az') != '00':
            login = "%s-%s" % (login, data.get('az'))
        body = MT %(login, data['passwort'])
        send_mail(sender, recipient, subject, body, file=None)
        self.flash(u'Die Mail wurde an das Mitglied versand')
        self.redirect(self.url(self.context, 'index'))
        

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
        e = self.request.get('e', 'm')
        if self.oid and e == 'm':
            sql = select([z1ext1ab],
                and_(z1ext1ab.c.trgrcd==self.oid,
                     z1ext1ab.c.az == self.az,
                     ))
            session = Session()
            self.obj = session.execute(sql).fetchone()
        if self.oid and e == 'e':
            sql = select([z1ext1ac],
                and_(z1ext1ac.c.oid==self.oid,
                     z1ext1ac.c.az == self.az,
                     ))
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
            funktion = self.obj.funktion,
            anr = self.obj.anr,
            titel = self.obj.titel,
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
                funktion=data.get('funktion'),
                titel=data.get('titel'),
                anr=data.get('anr'),
                email=data.get('email',)) 
                
        session = Session()
        session.execute(upd)
        e="m"
        if self.request.get('HTTP_REFERER', '').endswith('&e=e'):
            e="e"
        self.redirect(self.url(self.context, 'displayuser', dict(oid=data.get('oid'), az=data.get('az'), e=e)))

    @action(u'Abbrechen')
    def handle_cancel(self):
        self.flash(u'Aktion abgebrochen')
        self.redirect(self.application_url())
