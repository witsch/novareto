from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from nva.borrow import MessageFactory as _


# Interface class; used to define content-type schema.

class IBorrowableItems(form.Schema, IImageScaleTraversable):
    """
    Borrowable items
    """

    image = NamedImage(
            title=_(u"Image"),
            description=_(u"Image of the set"),
            required=True,
        )

    text = RichText(
            title=_(u'Text'),
            description=_(u'Verbose description of the set'),
            required=True)

    individualItemBooking = schema.Bool(
            title=_(u'Individual item booking possible'),
            description=_(u'Allow booking of individual items or only as set'),
            required=True,
            default=False)

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class BorrowableItems(dexterity.Container):
    grok.implements(IBorrowableItems)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# borrowableitems_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class IndexView(grok.View):
    grok.context(IBorrowableItems)
    grok.require('zope2.View')
    
    grok.name('view')
