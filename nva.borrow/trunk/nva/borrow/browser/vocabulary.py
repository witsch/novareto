from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName

class Vocabulary(BrowserView):

    def getData(self):                   
        catalog = getToolByName(self.context, 'portal_catalog')
        dl = atapi.DisplayList()
        for brain in catalog({'portal_type' : ['nva.borrow.borrowableitem', 'nva.borrow.borrowableitems']}):
            dl.add(brain.UID, brain.Title)
        return dl

