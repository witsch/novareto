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

class IContainerAnsprechpartner(form.Schema, IImageScaleTraversable):
    """
    Container fuer die Suche nach Ansprechpartnern
    """

    erlaeuterung = RichText(title=u"Nähere Erläuterung",
                            description = u"Hier können Sie Text eingeben, der oberhalb des Suchformulars angezeigt werden soll",
                            output_mime_type='text/html',
                            required=False,
                            )

class ContainerAnsprechpartner(Container):
    grok.implements(IContainerAnsprechpartner, IUVCAnsprechpartnersuche)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IContainerAnsprechpartner)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
