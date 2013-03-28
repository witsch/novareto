from zope import interface, schema
from zope.formlib import form
try:
    from five.formlib import formbase
except:    
    from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from nva.examplepack import examplepackMessageFactory as _

class ImyformSchema(interface.Interface):
    """ Definition der Schema-Felder """
    # -*- extra stuff goes here -*-
    name = schema.TextLine(title=u"Name", description=u"Bitte Namen eingeben.")
    ort = schema.TextLine(title=u"Ort", description=u"Bitte geben Sie den Ort ein.")


class myform(formbase.PageForm):
    form_fields = form.FormFields(ImyformSchema)
    label = _(u'Mein Beispiel Formular')
    description = _(u'Das ist ein Beispiel fuer ein generiertes Formular')

    @form.action('Absenden')
    def actionAbsenden(self, action, data):
        pass
        # Put the action handler code here 

    @form.action('Abbrechen')
    def actionAbbrechen(self, action, data):
        pass
        # Put the action handler code here 



