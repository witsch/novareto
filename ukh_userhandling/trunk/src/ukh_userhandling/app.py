# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grok
from megrok.layout import Page
from zeam.form.base import action
from dolmen.forms.base import ApplicationForm, Fields
from interfaces import IBenutzer
from ukh_userhandling import resource
import megrok.pagetemplate as pt
from megrok.menu import menuitem
from uvc.layout.slots.menus import GlobalMenu
from megrok import menu


grok.templatedir('templates')


class Ukh_userhandling(grok.Application, grok.Container):
    pass


from zope.interface import Interface

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
        data, errors = self.extractData()
        if errors:
            return errors
        print "BLA"



class AsPdf(grok.View):
    grok.name('pdf')
    menu.menuitem('documentactions', icon="fanstatic/example/icons/pdf.png")

    def render(self):
        return "I Should BE A PDF"
