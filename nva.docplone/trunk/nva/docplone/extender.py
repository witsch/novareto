# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.atapi import ATFieldProperty 
from Products.ATContentTypes.content.document import ATDocument
from nva.docplone.field import DocPloneField
from nva.docplone.widget import DocPloneWidget

class PageExtender(object):
    adapts(ATDocument)
    implements(ISchemaExtender)


    fields = [
        DocPloneField("doczeichen",
        schemata="categorization",
        widget = DocPloneWidget(
            label=u"Vergabe von DOK-Zeichen für den Artikel",
            label_msgid='label_doczeichen',
            i18n_domain='nva.docplone',)),
            ]


    #doczeichen = ATFieldProperty('doczeichen')

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields

