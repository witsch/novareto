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

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from borrowableitem import IBorrowableItem

@grok.provider(IContextSourceBinder)
def borrowableItems(context):
    items = list()
    items.append(SimpleVocabulary.createTerm(u'a', u'b'))
    items.append(SimpleVocabulary.createTerm(u'c', u'd'))
    return SimpleVocabulary(items)



# Interface class; used to define content-type schema.

class IBorrowRequest(form.Schema, IImageScaleTraversable):
    """
    Request to borrow items
    """

    firstName = schema.TextLine(
        title=_(u'First name'),
        required=True,
        default=u'')   

    lastName = schema.TextLine(
        title=_(u'Last name'),
        required=True,
        default=u'')   

    address = schema.TextLine(
        title=_(u'Address'),
        required=True,
        default=u'')   

    zip = schema.TextLine(
        title=_(u'ZIP code'),
        required=True,
        default=u'')   

    city = schema.TextLine(
        title=_(u'City'),
        required=True,
        default=u'')   

    phone = schema.TextLine(
        title=_(u'Phone'),
        required=False,
        default=u'')   

    email = schema.TextLine(
        title=_(u'Email'),
        required=False,
        default=u'')   

    memberId= schema.TextLine(
        title=_(u'Member id'),
        description=_(u'Member ID'),
        required=True,
        default=u'00000')   

    borrowFrom = schema.Date(
        title=_(u'Borrow from'),
        required=True,
        default=None)

    borrowTo = schema.Date(
        title=_(u'Borrow to'),
        required=True,
        default=None)

    borrowItems = RelationList(
        title=_(u'Items to borrow'),
        default=[],
        value_type=RelationChoice(title=_(u'Related'),
                                  source=ObjPathSourceBinder(object_provides=IBorrowableItem.__identifier__))
            )

    comment = schema.Text(
        title=_(u'Comment'),
        description=_(u'Comment'),
        required=False,
        default=u'')   

    @invariant
    def validateStartEnd(data):
        if data.borrowFrom is not None and data.borrowTo is not None:
            if data.borrowFrom > data.borrowTo:
                raise Invalid(_(u"The start date must be before the end date."))

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class BorrowRequest(dexterity.Item):
    grok.implements(IBorrowRequest)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# borrowrequest_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(IBorrowRequest)
    grok.require('zope2.View')
    
    # grok.name('view')
