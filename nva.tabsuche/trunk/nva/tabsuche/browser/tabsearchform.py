# -*- coding:utf-8 -*-
# author: lwalther@novareto.de

import re
from zope import interface, schema
from zope.formlib import form
try:
    from Products.Five.formlib import formbase
except:
    from five.formlib import formbase
from Products.Five.browser import pagetemplatefile
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.schema import ValidationError
from nva.tabsuche import tabsucheMessageFactory as _
from nva.tabsuche.lib.tabreader import findTabByPlz, findTabByOrt, findRehaByPlzName
from zope.interface import implements

class NotValidEingabePLZ(ValidationError):
    u""" Ihre eingegebene Postleitzahl entspricht nicht dem geforderten Format (5-stellig numerisch)
         oder der angegebene PLZ-Bereich ist ungültig. Bitte überprüfen Sie ihre Eingabe.
    """

def validatePLZ(value):
    """ Der nachfolgende RegEx Ausdruck validiert die PLZ wie folgt:
        True: Alle Zahlen die 5 stellig sind und keinen Buchstaben haben
        False: ABC12 | 1234a | 1 
    """
    checkplz = re.compile(r'^([0]{1}[1-9]{1}|[1-9]{1}[0-9]{1})[0-9]{3}$').match
    if not bool(checkplz(value)):
        raise NotValidEingabePLZ(value)
    excludes = [{'lo':0, 'hi':999}, {'lo':5000, 'hi':5999}, {'lo':11000, 'hi':11999}, 
                {'lo':43000, 'hi':43999}, {'lo':62000, 'hi':62999}]
    for i in excludes:
        if i['lo'] <= int(value) <= i['hi']:
            raise NotValidEingabePLZ(value)           
    return True

class NotValidEingabeOrt(ValidationError):
    u""" Eine erfolgreiche Suche nach dem eingegebenen Ortsnamen ist leider nicht möglich, bitte 
         überprüfen Sie Ihre Eingabe.
     """

def validateOrt(value):
    """ Die nachfolgende Validierung prueft, ob der Ortsname mindestens 3 Buchstaben enthaelt,
        wenn es sich nicht um den Ortsnamen Au handelt. 
    """
    if len(value) < 3:
        if value not in ['au', 'Au']:
            raise NotValidEingabeOrt(value)
    else:
        if not value.isalpha():
            raise NotValidEingabeOrt(value)
    return True

class NotValidEingabeName(ValidationError):
    u""" Bitte überprüfen Sie Ihre Eingabe. Ein gültiger Name muss aus mindestens 2 Buchstaben bestehen."""

def validateName(value):
    """ Die nachfolgende Validierung prueft, ob es sich beim Namen um
        eine Kombination von Buchstaben handelt. 
    """
    if not value.isalpha() or len(value) < 2:
        raise NotValidEingabeName(value)
    return True


class ITABSearchFormSchema(interface.Interface):
    # -*- extra stuff goes here -*-
    tabplz = schema.TextLine(title=_(u'Postleitzahl'),
                          description=_(u'Bitte geben Sie hier eine 5-stellige Postleitzahl ein fuer die Sie einen Berater unserer Praevention suchen.'),
                          required = False,
                          constraint = validatePLZ,
                          )
    tabort = schema.TextLine(title=_(u'Ort'),
                         description=_(u'Sollten Sie nicht ueber die Postleitzahl verfuegen, koennen Sie alternativ hier auch nach einem Ortsnamen suchen'),
                         required = False,
                         constraint = validateOrt,
                         ) 

class TABSearchForm(formbase.PageForm):
    form_fields = form.FormFields(ITABSearchFormSchema)
    result_template = pagetemplatefile.ZopeTwoPageTemplateFile('tab-results.pt')
    label = _(u'TAB-Suche')
    description = _(u'Suche nach dem Praeventionsmitarbeiter')

    @form.action('Suche')
    def actionSubmit(self, action, data):
        fileobject = False
        if self.context.portal_type == 'File':
            fileobject = self.context.getFile()
        self.plzresults = {}
        self.ortresults = []
        self.retval = False
        if data['tabplz']:
            self.plzresults = findTabByPlz(data['tabplz'], fileobject)
        if data['tabort']:
            self.ortresults = findTabByOrt(data['tabort'], fileobject)
        if self.plzresults or self.ortresults:
            self.retval = True
        return self.result_template()

class IREHASearchFormSchema(interface.Interface):
    # -*- extra stuff goes here -*-
    rehaplz = schema.TextLine(title=_(u'Postleitzahl'),
                          description=_(u'Bitte geben Sie hier eine 5-stellige Postleitzahl fuer den Wohnort des Versicherten ein.'),
                          required = True,
                          constraint = validatePLZ,
                          )
    nachname = schema.TextLine(title=_(u'Nachname'),
                         description=_(u'Bitte geben Sie hier den Nachnamen des Versicherten ein.'),
                         required = True,
                         constraint = validateName,
                         )

class REHASearchForm(formbase.PageForm):
    form_fields = form.FormFields(IREHASearchFormSchema)
    template = pagetemplatefile.ZopeTwoPageTemplateFile('reha-search.pt')
    result_template = pagetemplatefile.ZopeTwoPageTemplateFile('reha-results.pt')
    label = _(u'REHA-Suche')
    description = _(u'Suche nach einer Bezirksverwaltung')

    @form.action('Suche')
    def actionSubmit(self, action, data):
        fileobject = False
        if self.context.portal_type == 'File':
            fileobject = self.context.getFile()
        results = findRehaByPlzName(data['rehaplz'], data['nachname'], fileobject)
        self.rd = results.get('rd', '')
        self.strnr = results.get('strnr', '')
        self.plzort = "%s %s" % (results.get('plz', ''), results.get('ort', ''))
        self.tel = results.get('tel', '')
        self.fax = results.get('fax', '')
        return self.result_template()
