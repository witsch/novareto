# -*- coding: utf-8 -*-
from five import grok
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from bghw.ansprechpartner.interfaces import IUVCAnsprechpartnersuche

from bghw.ansprechpartner import MessageFactory as _


# Interface class; used to define content-type schema.

class IExcelDatenbasis(form.Schema, IImageScaleTraversable):
    """
    Der Ansprechpartnersuche wird eine Excel-Datenbasis hinzugefuegt
    """

    excelfile = NamedBlobFile(
            title = _(u"Excel-Datei"),
            description = _(u"Bitte laden Sie hier die Excel-Datei mit den Daten hoch."),
            required = True,
            )


    abteilung = schema.Choice(
            title = _(u"Abteilung"),
            description = _(u"Bitte wählen Sie hier die Abteilung aus, deren Daten mit der hochgeladenen\
                    Datei angezeigt werden sollen. Vorsicht: eine falsche Auswahl kann durch\
                    Fehlinterpretation der Excel-Daten zu einem Anzeigefehler führen."),
            vocabulary = SimpleVocabulary.fromValues([u'Praevention', u'Reha/Leistung', u'MuB', 
                                                      u'BK', u'Regress']),
            required = True,
            )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ExcelDatenbasis(Container):
    grok.implements(IExcelDatenbasis, IUVCAnsprechpartnersuche)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# excel_datenbasis_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IExcelDatenbasis)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
