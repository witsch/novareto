from zope.formlib import form
from zope.interface import implementedBy
from zope.schema.fieldproperty import FieldProperty
	

def setDefaultFields(cls, interfaces=None):
    if not interfaces:
        interfaces = list(implementedBy(cls))
        
    formfields = form.FormFields(*interfaces)
    for formfield in formfields:
        fname = formfield.__name__
        if not hasattr(cls, fname):
            setattr(cls, fname, FieldProperty(formfield.field))
