import random
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from datetime import datetime, timedelta
import ics

class Orders(BrowserView):

    def getDateRange(self, start_date=None, start_offset_days=14, num_days=30):
        """ Calculate the day range for the matrix based on a given 'start_date'
            or <current date> + <start_offset_days> (2 weeks by default)

        """
        if not start_date:
            start_date = datetime.now() + timedelta(days=start_offset_days)
        return ics.getDateRange(start_date, num_days)

    def getItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'portal_type' : ['nva.borrow.borrowableitem']})
        objs = [brain.getObject() for brain in brains]
        category = self.request.get('category')
        if category:
            objs = [o for o in objs if category in o.categories]
        return objs

    def getItemIds(self):
        return [item.restrictedTraverse('@@getIntId')() for item in self.getItems()]

    def random(self, upper=1):
        return random.randint(0, upper)

    def processBooking(self):
        booking_bolder = self.context['bookings']
        self.request.response.redirect('%s/order-form' % self.context.absolute_url())

