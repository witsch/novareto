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


from bghw.mediashop import MessageFactory as _


# Interface class; used to define content-type schema.

class IArtikel(form.Schema, IImageScaleTraversable):
    """
    Artikel im Medienshop
    """
    beschreibung = RichText(
                       title=u'Artikelbeschreibung',
                       description=u'Bitte formulieren Sie hier eine ausführliche Beschreibung\
                                     für den Artikel.',
                       required = False,
                       )

    bestellnummer = schema.TextLine(
                       title=u'Bestellnummer',
                       description=u'Bitte tragen Sie hier die Bestellnummer oder Kurzbezeichnung für den\
                                     Artikel ein.',
                       required = True,
                       )

    artikelnummer = schema.TextLine(
                       title=u'Artikelnummer',
                       description=u'Bitte tragen Sie hier die Artikelnummer aus dem Warenwirtschaftssystem ein.',
                       required = True,
                       )

    stand = schema.TextLine(
                       title=u'Stand',
                       description=u'Bitte geben Sie hier Informationen zum Stand, Bsp.: Ausgabedatum\
                                      des Mediums ein.',
                       required = False,
                       )

    bild = NamedBlobImage(
                       title=u"Bild",
                       description=u"Hier können Sie ein Bild des Mediums hochladen.",
                       required = False,
                       )

    fileref = RelationChoice(
                       title=u"Dateireference",
                       description=u"Bitte wählen Sie hier eine Referenz zu einem Dateiobjekt aus.",
                       source = ObjPathSourceBinder(),
                       required = False,
                       )

    maxquantitiy = schema.Int(
                       title=u"Maximale Bestellmenge",
                       description=u"Bitte geben Sie hier die maximale Bestellmenge ein.",
                       default=999,
                       required = True,
                       )

    status = schema.Choice(
                       title=u"Artikelstatus",
                       description=u"Bitte wählen Sie hier einen Status für den Artikel aus.",
                       default = u'lieferbar',
                       vocabulary = SimpleVocabulary.fromValues([u'lieferbar', 
                                                                 u'nicht lieferbar', 
                                                                 u'nur Download']),
                       required = True,
                       )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Artikel(Container):
    grok.implements(IArtikel)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# artikel_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class ArtikelView(grok.View):
    """ sample view class """

    grok.context(IArtikel)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
