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


grok.templatedir('templates')


class Ukh_userhandling(grok.Application, grok.Container):
    pass


from zope.interface import Interface

class Index(ApplicationForm):
    grok.context(Interface)
    grok.title(u'Benutzer Verwaltung')
    grok.description(u'BLA BLA')
    label = u"Benutzerverwaltung"
    description = u"Hier können Sie Benuzterdaten verwalten"
    legend = u"Bitte die Suchkriterien eingeben"
    menuitem('oter')

    fields = Fields(IBenutzer)

    @action(u'Suchen')
    def handel_search(self):
        data, errors = self.extractData()
        if errors:
            return errors
        print "BLA"



class FormTemplate(pt.PageTemplate):
    """Template for a layout aware form.
    """
    pt.view(ApplicationForm)

