from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IVocabulary
from Products.CMFCore.utils import getToolByName
from Products.PFGDataGrid.vocabulary import SimpleDynamicVocabulary

class DynamicVocabulary(SimpleDynamicVocabulary):

    implements(IVocabulary)
    
    def __init__(self, displaylist):
        """ @values - simple list of values """
        self._values = displaylist.values()
        self._values_dl =  displaylist



class Vocabulary(BrowserView):

    def getData(self):                   

        catalog = getToolByName(self.context, 'portal_catalog')
        import pdb; pdb.set_trace() 
        dl = atapi.DisplayList()
        for brain in catalog({'portal_type' : ['nva.borrow.borrowableitem', 'nva.borrow.borrowableitems']}):
            dl.add(brain.getId, brain.Title)
        return DynamicVocabulary(dl)

