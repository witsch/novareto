# -*- coding: iso-8859-1 -*-

import time
from datetime import date

from five import grok
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import invariant, Invalid
from z3c.form import group, field
from z3c.relationfield.schema import RelationList, RelationChoice

from plone.app.textfield import RichText
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.ATContentTypes.interfaces.image import IImageContent
from Products.CMFCore.utils import getToolByName

from nva.borrow import MessageFactory as _
import config

# Interface class; used to define content-type schema.

MONTH_NAMES = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 
               'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

categoryItems = SimpleVocabulary([SimpleVocabulary.createTerm(cat, cat) 
                                 for cat in config.CATEGORIES])


class IBorrowableItem(form.Schema, IImageScaleTraversable):
    """ Borrowable item """

    text = RichText(
            title=_(u'Text'),
            description=_(u'Verbose description of the set'),
            required=True)
    
    itemsAvailable = schema.Int(
        title=_(u'Items available'),
        description=_(u'Items available'),
        required=True,
        min=0,
        max=10,
        default=1)   
 
    maxItemsBorrowable = schema.Int(
        title=_(u'Max number of items that can be borrowed'),
        description=_(u'A person can only borrow a max number of items each'),
        required=True,
        min=1,
        max=20,
        default=1)   
 
    imageReferences = RelationList(
                title=_(u'Image references (experimental)'),
                description=_(u'Image references (experimental)'),
                value_type=RelationChoice(title=u'Images', source=ObjPathSourceBinder(object_provides=IImageContent.__identifier__)),
                required=False)

    categories = schema.List(
                    title=u'Categories',
                    value_type=schema.Choice(vocabulary=categoryItems),
                    required=True)


class BorrowableItem(dexterity.Item):
    grok.implements(IBorrowableItem)
    
    # Add your class methods and properties here
                                
    def getBorrowRequests(self):
        """ Return all borrow requests referencing the current item"""
        from Acquisition import aq_inner
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds
        from zope.security import checkPermission
        from zc.relation.interfaces import ICatalog

        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        for rel in catalog.findRelations(
                                dict(to_id=intids.getId(aq_inner(self)),
                                     )
                                ):
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result 

    def isBorrowable(self, start=None, end=None):
        """ Is current item borrowable from start-end ?"""
        start = date(2012,8,10)
        end = date(2012,8,17)
        conflicting_requests = list()
        for request in self.getBorrowRequests():
            if request.buchungStart > end or request.buchungEnde < start:
                continue
            conflicting_requests.append(request)
        return self.itemsAvailable > len(conflicting_requests)

    def getBookingDates(self):
        """ Return all booking dates for this particular item """

        intid = str(self.restrictedTraverse('@@getIntId')())
        bookings = list()
        catalog = getToolByName(self, 'portal_catalog')
        for brain in catalog({'portal_type' : 'nva.borrow.borrowrequest'}):
            br = brain.getObject()
            for d in eval(br.formData)['items']:
                if d['id'] == intid and br.buchungStart:
                    bookings.append(dict(fromDate=br.buchungStart,
                                         toDate=br.buchungEnde,
                                         url=br.absolute_url(),
                                         title=br.Title(),
                                         numberItems=int(d['number'])))

        bookings.sort(lambda x,y: cmp(time.strptime(x['fromDate'], '%d.%m.%Y'),
                                      time.strptime(y['fromDate'], '%d.%m.%Y')))
        return bookings


class IndexView(grok.View):
    grok.context(IBorrowableItem)
    grok.require('zope2.View')
    grok.name('view')
