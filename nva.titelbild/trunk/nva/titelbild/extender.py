# -*- coding: utf-8 -*-
# Copyright (c) 2004-2013 novareto GmbH
# lwalther@novareto.de
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.public import StringWidget, SelectionWidget, ImageWidget, BooleanWidget, ReferenceWidget
from Products.Archetypes.atapi import StringField, ReferenceField, ImageField, BooleanField, LinesField
from Products.Archetypes.atapi import DisplayList
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content.base import ATCTMixin
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.topic import ATTopic
from Products.ATContentTypes.content.document import ATDocument

from Products.Archetypes.atapi import AnnotationStorage
from Products.ATContentTypes.configuration import zconf

from Products.validation import V_REQUIRED

from nva.titelbild import titelbildMessageFactory as _

from archetypes.schemaextender.field import ExtensionField

class CustomStringField(ExtensionField, StringField):
    pass

class CustomImageField(ExtensionField, ImageField):
    pass

class CustomBooleanField(ExtensionField, BooleanField):
    pass

class CustomReferenceField(ExtensionField, ReferenceField):
    pass

class CustomLinesField(ExtensionField, LinesField):
    pass


extension_fields = [
               CustomReferenceField('titleimages',
               schemata='Medien',
               relationship='rel_titleimages',
               multiValued=True,
               widget = ReferenceBrowserWidget(
                           label = _(u"Titelbilder"),
                           description = _(u"Bitte waehlen Sie hier Bilder fuer die Anzeige im Titel des Ordners."),
                           startup_directory = '/',
                           destination_types = ('Image',),
                           force_close_on_insert = True,
                           ),
                 ),
               CustomBooleanField('anzeige',
               schemata='Medien',
                   default = True,
                   widget = BooleanWidget(
                        label = u"Anzeige des Titelbildes im Ordner",
                        description = u"Auswahl wenn das Titelbild im Ordner angezeigt werden soll. Ist kein Bild vorhanden wird \
                                        das Bild in einem darueber liegenden Ordner angezeigt",
                        ),
                 ),
               CustomBooleanField('spalte',
               schemata='Medien',
                   default = False,
                   widget = BooleanWidget(
                        label = u"Anzeige in der linken Spalte?",
                        description = u"Auswahl wenn das Bild (die Bilder) in der linken Spalte der zweispaltigen Ordneransicht \
                                        angezeigt werden soll(en)",
                        ),
                 ),
               CustomBooleanField('zufall',
               schemata='Medien',
                   default = True,
                   widget = BooleanWidget(
                        label = u"Zufaellige Reihenfolge der Titelbilder",
                        description = u"Auswahl wenn das angezeigte Titelbild nach dem Zufallsprinzip ausgewahlt werden soll.",
                        ),
                 ),
               CustomReferenceField('videopath',
               schemata='Medien',
               relationship='rel_videopath',
               multiValued=True,
               widget = ReferenceBrowserWidget(
                           label = _(u"Pfad zum Video"),
                           description = _(u"Bitte waehlen Sie aus, mit welchem Videoobjekt das Titelbild verlinkt werden soll."),
                           startup_directory = '/',
                           force_close_on_insert = True,
                           ),                  ),
               CustomReferenceField('imagepath',
               schemata='Medien',
               relationship='rel_imagepath',
               multiValued=True,
               widget = ReferenceBrowserWidget(
                           label = _(u"Pfad zur Bildergalerie"),
                           description = _(u"Bitte waehlen Sie aus, mit welcher Bildergalerie das Titelbild verlinkt werden soll."),
                           startup_directory = '/',
                           force_close_on_insert = True,
                           ),
                  ),]

class FolderImageExtender(object):
    adapts(ATFolder)
    implements(ISchemaExtender)
    fields = extension_fields

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields

class TopicImageExtender(object):
    adapts(ATTopic)
    implements(ISchemaExtender)
    fields = extension_fields

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields


class DocumentImageExtender(object):
    adapts(ATDocument)
    implements(ISchemaExtender)
    fields = extension_fields

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields

