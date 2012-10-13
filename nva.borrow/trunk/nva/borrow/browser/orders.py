from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from datetime import datetime
import ics

class Orders(BrowserView):

    def getDateRange(self, num_days=30):
        return ics.getDateRange(datetime.now().date(), num_days)

    def getItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog({'portal_type' : ['nva.borrow.borrowableitem']}, full_objects=True)
