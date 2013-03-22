# -*- coding: utf-8 -*-
from zope.interface import implements, Interface, invariant, Invalid
from zope import schema
from zope.formlib import form
from five.formlib import formbase
from plone.fieldsets.fieldsets import FormFieldsets
from plone.fieldsets.form import FieldsetsInputForm, FieldsetsEditForm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.app.form.browser import RadioWidget as _RadioWidget
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent
from nva.bsbetreuung.wizard import getStep, prepareData, calculateStep, saveStepData, eraseStepData
from nva.bsbetreuung.interfaces import IProgress
from nva.bsbetreuung import bsbetreuungMessageFactory as _


def RadioWidget(field, request):
    """angepasstes Widget fuer das einleitende Auswahlfeld"""
    vocabulary = field.vocabulary
    widget = _RadioWidget(field, vocabulary, request)
    return widget

def getOptionsVocab(comp_field):
    """aus dem Feld Optionen wird ein Vocabulary fuer das Schema-Feld erzeugt"""
    terms = []
    for i in comp_field.getOptionen():
        terms.append(SimpleTerm(value = i.split('|')[0].decode('utf-8'), title=i.split('|')[1].decode('utf-8')))
    return SimpleVocabulary(terms)

class IBasis(Interface):
    """
    Interface zur Beschreibung des Auswahlfeldes
    """
    mybool = schema.Choice(title=u'Trifft mindestens eines der vorgenannten Kriterien auf Ihren Betrieb zu?',
                           description=u'', values=(u'ja', u'nein'))


class aufgabeView(FieldsetsInputForm):
    """
    aufgabe browser view
    """
    implements(IProgress)
    template = ViewPageTemplateFile('aufgabe_form.pt')
    label = _(u'TAB-Suche')
    description = _(u'Suche nach dem Praeventionsmitarbeiter')

    def __init__(self, context, request):
        self.context, self.request = context, request
        basisset = FormFieldsets(IBasis)
        basisset.label = u'Bitte treffen Sie eine Auswahl'
        basisset.id = u'hh_basis'
        comp_fields = self.getFragenInOrder()
        myfields = []
        self.faktoren = {}
        self.field_help = {}
        for i in comp_fields:
            if i.fieldtype == 'choice':
                myfields.append(schema.Choice(__name__=i.id, title=i.title.decode('utf-8'),
                                              vocabulary=getOptionsVocab(i), required=True,))
            elif i.fieldtype == 'float':
                myfields.append(schema.Float(__name__=i.id, title=i.title.decode('utf-8'), min = 0.0, required=True,))
            elif i.fieldtype == 'textline':
                myfields.append(schema.TextLine(__name__=i.id, title=i.title.decode('utf-8'), required=False,))
            elif i.fieldtype == 'text':
                myfields.append(schema.Text(__name__=i.id, title=i.title.decode('utf-8'), required=False,))
            self.faktoren[i.id] = i.faktor
            self.field_help[i.id] = i.getHilfe()
        if myfields:
            myfields = form.Fields(*myfields)
            aufgabenset = FormFieldsets(myfields)
            aufgabenset.label = u'Bitte beantworten Sie die Fragen'
            aufgabenset.id = u'hh_fragen'
            self.form_fields = FormFieldsets(basisset, aufgabenset)
        else:
            self.form_fields = FormFieldsets(basisset)
        self.form_fields['mybool'].custom_widget = RadioWidget

    def getFragenInOrder(self):
        """Funktion wird aktuell gebraucht weil die Fragen aus dem Attribut nicht geordnet kommen"""
        fragen = []
        if self.context.portal_type == 'Aufgabe':
            fragen = self.context.getFragen()
            references_order = self.context.getRefs()
            fragen = [i for i in references_order if i in fragen]
        return fragen

    def validate(self, action, data):
        """ Validation-Hook wegen der besonderen Bedeutung der Vorauswahl 
            und der Zurueck-Funktion des Wizard """
        if action.label == u'Zurück':
            return []
        if self.request.get('form.mybool') == 'nein':
            return []
        return (form.getWidgetsData(self.widgets, self.prefix, data) +
                form.checkInvariants(self.form_fields, data))

    @form.action(u'Zurück')
    def actionSubmit(self, action, data):
        stepnr = self.context.nummer
        cookie = eraseStepData(self.context, stepnr)
        folder = self.context.aq_inner.aq_parent
        objects = folder.listFolderContents()
        doclist = []
        for i in objects:
            if i.portal_type == 'Aufgabe':
                doclist.append(i)
        next = getStep(doclist, self.context, 'backward')
        if next == 'redir':
            return self.request.response.redirect(self.getStartFinalPage())
        return self.request.response.redirect(doclist[next].absolute_url())


    @form.action(u'Weiter')
    def actionSubmit(self, action, data):
        stepnr = self.context.nummer
        basis = self.context.basiszeitfaktor
        min = self.context.minimum
        max = self.context.maximum
        alt = self.context.alternativtext
        if data:
            valuedata, commentdata = prepareData(self.context.fragen)
            stepvalue = calculateStep(self.context, valuedata, data, basis, min, max)
            cookie = saveStepData(self.context, stepnr, valuedata, commentdata, data, stepvalue, alt)
        folder = self.context.aq_inner.aq_parent
        objects = folder.listFolderContents()
        doclist = []
        for i in objects:
            if i.portal_type == 'Aufgabe':
                doclist.append(i)
        next = getStep(doclist, self.context, 'forward')
        if next == 'redir':
            return self.request.response.redirect(self.getStartFinalPage())
        return self.request.response.redirect(doclist[next].absolute_url())

    def getStartFinalPage(self):
        """
        Ermittelt die Weiterleitung zu einer Start- bzw. Abschlussseite
        und gibt diese an die Action zurueck
        """
        obj = self.context.startend
        url = self.context.absolute_url()
        if obj:
            if isinstance(obj, list):
                url = obj[0].absolute_url()
            else:
                url = obj.absolute_url()
        return url

 
