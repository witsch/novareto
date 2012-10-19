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

class IItemContainer(form.Schema, IImageScaleTraversable):
    """
    Container for borrowable items
    """

BOOKING_ID = 'bookings'
ORDERFORM_ID = 'order-form'

class ItemContainer(dexterity.Container):
    grok.implements(IItemContainer)
    
    def manage_afterAdd(self, container, item):
        if self.getId() != BOOKING_ID and not BOOKING_ID  in container.objectIds():
            self.invokeFactory('Folder', id=BOOKING_ID, title='Bookings')
            bookings = self[BOOKING_ID]

        if not ORDERFORM_ID in container.objectIds():
            self.restrictedTraverse('@@setupPFG')(ORDERFORM_ID)

class SampleView(grok.View):
    grok.context(IItemContainer)
    grok.require('zope2.View')
    
    # grok.name('view')
