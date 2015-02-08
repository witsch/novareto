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


from nva.iframe import MessageFactory as _


# Interface class; used to define content-type schema.

class IiFrameLink(form.Schema, IImageScaleTraversable):
    """
    A URL rendered as iFrame
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/iframe_link.xml to define the content type.

    src = schema.URI(title = u'Quell-URL für den iFrame',
            required = True)

    callid = schema.TextLine(title = u'CallID',
            description = u'Bitte tragen Sie hier, falls vorhanden, den Wert fuer den Parameter CallID ein',
            required = False)

    width = schema.TextLine(title = u'Breite des iFrames',
            required = True)

    height = schema.TextLine(title = u'Höhe des iFrames',
            required = True)

    cssfile = NamedBlobFile(title = u'CSS-File',
            description = u'Hier können Sie ein CSS-File hochladen, um die Inhalte des iFrames\
                          optisch anzupassen',
            required = False)

    showtitle = schema.Bool(title = u'Titel anzeigen',
            description = u"Hier klicken wenn der Titel des iFrame-Objektes angezeigt werden soll.",
            required = False)

    showdescription = schema.Bool(title = u'Beschreibung anzeigen',
            description = u"Hier klicken wenn die Beschreibung des iFrame-Objektes angezeigt werden soll.",
            required = False)

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class iFrameLink(Container):
    grok.implements(IiFrameLink)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# iframe_link_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IiFrameLink)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
