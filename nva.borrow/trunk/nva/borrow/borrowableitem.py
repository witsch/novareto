# -*- coding: iso-8859-1 -*-

import time
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

from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

# Interface class; used to define content-type schema.

MONTH_NAMES = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 
               'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

class IBorrowableItem(form.Schema, IImageScaleTraversable):
    """
    Borrowable item
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/borrowableitem.xml to define the content type
    # and add directives here as necessary.
    
#    form.model("models/borrowableitem.xml")
    
    itemsAvailable = schema.Int(
        title=_(u'Items available'),
        description=_(u'Items available'),
        required=True,
        min=1,
        max=10,
        default=1)   
 
    image = NamedImage(
            title=_(u"Image"),
            description=_(u"Image of the item"),
            required=True,
        )

    text = RichText(
            title=_(u'Text'),
            description=_(u'Verbose description of the set'),
            required=True)


class BorrowableItem(dexterity.Item):
    grok.implements(IBorrowableItem)
    
    # Add your class methods and properties here
                                
    def getBorrowRequests(self):
        """ Return all borrow requests referencing the curret item"""
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
        from datetime import date
        start = date(2012,8,10)
        end = date(2012,8,17)
        conflicting_requests = list()
        for request in self.getBorrowRequests():
            print request.borrowFrom, request.borrowTo
            if request.borrowFrom > end or request.borrowTo < start:
                continue
            conflicting_requests.append(request)
        return self.itemsAvailable > len(conflicting_requests)

    def getBookingDates(self):
        """ Return all booking dates for this particular item """
        bookings = [dict(fromDate=request.borrowFrom.strftime('%d.%m.%Y'), 
                         toDate=request.borrowTo.strftime('%d.%m.%Y'))
                    for request in self.getBorrowRequests()]
        bookings.sort(lambda x,y: cmp(time.strptime(x['fromDate'], '%d.%m.%Y'),
                                      time.strptime(y['fromDate'], '%d.%m.%Y')))
        return bookings

    def getBookingCalendar(self):
        """ return a booking calendar data structure """

        import calendar
        from datetime import datetime, date, timedelta

        booking_requests = self.getBorrowRequests()

        result = list()
        now = datetime.now().replace(day=15)
        for num in range(0, 12):
            next_first = (now + timedelta(days=30*num)).replace(day=1)
            days_in_month = calendar.monthrange(next_first.year, next_first.month)[1]
            print next_first, days_in_month
            d = dict(year=next_first.year, month=next_first.month, month_name=MONTH_NAMES[next_first.month-1], days=[])
            for day in range(1, days_in_month+1):
                current_day = date(next_first.year, next_first.month, day)


                # default status
                status = 'free'
                # check against booking requests
                for request in booking_requests:
                    if request.borrowFrom <= current_day and current_day <= request.borrowTo:
                        status = 'blocked'
                        break

                if current_day.weekday() in [5,6]:
                    status = 'weekend'
                d['days'].append(dict(day=current_day.day, 
                                      weekday=current_day.weekday(),
                                      status=status))
            result.append(d)

        return result

# View class
# The view will automatically use a similarly named template in
# borrowableitem_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class IndexView(grok.View):
    grok.context(IBorrowableItem)
    grok.require('zope2.View')
    
    grok.name('view')
