# -*- coding: utf-8 -*-

import five.grok as grok

from zope.interface import Interface
from z3c.form import form, field, button
from nva.mediashop.interfaces import IOrderForm
from collective.z3cform.grok.grok import PloneFormWrapper
from plone.z3cform.fieldsets.extensible import ExtensibleForm


grok.templatedir('templates')

class BasicForm(ExtensibleForm, form.Form):
    """A z3c.form"""
    ignoreContext = True
    fields = field.Fields(IOrderForm) 
    label = u"Bestellformular"

    @button.buttonAndHandler(u'Zurück zum Warenkorb')
    def handleBack(self, action):
        data, errors = self.extractData()

    @button.buttonAndHandler(u'Bestellung senden')
    def handleOrder(self, action):
        data, errors = self.extractData()

    @button.buttonAndHandler(u'Abbrechen')
    def handleCancel(self, action):
        data, errors = self.extractData()


class OrderForm(PloneFormWrapper):
    grok.context(Interface)
    form = BasicForm

    def renderField(self, field):
        field = self.form.fields.get(field)
        import pdb; pdb.set_trace() 
