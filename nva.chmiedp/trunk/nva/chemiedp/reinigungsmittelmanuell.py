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


from nva.chemiedp import MessageFactory as _
from nva.chemiedp.vocabularies import anwendungsgebieteVocab
from nva.chemiedp.hersteller import IHersteller

# Interface class; used to define content-type schema.

class IReinigungsmittelManuell(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """

    hersteller = RelationChoice(title = _(u"Hersteller"),
            description = _(u"Bitte wählen Sie hier den Hersteller des Reinigungsmittels aus."),
            source=ObjPathSourceBinder(object_provides=IHersteller.__identifier__),
            required = True,)

    anwendungsgebiete = schema.List(title = _(u"Anwendungsgebiete"),
            description = _(u"Bitte wählen Sie die Anwendungsgebiete des Reinigungsmittels aus."),
            value_type = schema.Choice(title = _(u"Anwendungsgebiet"),
                                       vocabulary = anwendungsgebieteVocab),
            required = True,)

    flammpunkt = schema.Int(title = _(u"Flammpunkt"),
            description = _(u"Bitte geben Sie hier den Wert des Flammpunktes in Grad Celsius an."),
            required = False,)

    wertebereich = schema.Bool(title = _(u"Wertebereich für den Flammpunkt"),
            description = _(u"Bitte treffen Sie hier eine Auswahl wenn der Wertebereich für den\
                              Flammpunkt größer als der angegebene Zahlenwert ist."),
            required = False,)

    emissionsgeprueft = schema.Bool(title = _(u"Emissionsarmes Produkt"),
            description = _(u"Bitte markieren Sie hier, wenn für das Produkt die Kriterien des Gütesiegels\
                              erfüllt sind."),
            required = False,)


class ReinigungsmittelManuell(Container):
    grok.implements(IReinigungsmittelManuell)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# reinigungsmittelmanuell_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IReinigungsmittelManuell)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
