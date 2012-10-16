from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from .. import config

class Categories(BrowserView):

    def getCategories(self):
        return config.CATEGORIES

    def itemsWithCategory(self, category):
        items = list()
        catalog = getToolByName(self.context, 'portal_catalog')
        for brain in catalog({'portal_type' : 'nva.borrow.borrowableitem'}):
            item = brain.getObject()
            if category in item.categories:
                items.append(item)
        return items
    
    def getAllItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return [brain.getObject() for brain in catalog({'portal_type' : 'nva.borrow.borrowableitem'})]
