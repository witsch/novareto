# -*- coding: utf-8 -*-
from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic
from plone.app.collection.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish


grok.templatedir('templates')

class Accordion_View(uvcsite.Page):
    grok.context(Interface)
    grok.title('Accordion-Ansicht')

    @property
    def query(self):
        """ 
        Make catalog query for the folder listing.
        """
        if IATTopic.providedBy(self.context) or ICollection.providedBy(self.context):
            return self.context.queryCatalog(batch=False)
        elif IFolderish.providedBy(self.context):
            return self.context.getFolderContents(batch=False)

    def update(self):
        """
        Create Objectlist for the Accordion
        """
        brains = self.query
        items_with_bodytext = ['Document', 'News Item']
        counter = 1
        objectlist = []
        for i in brains:
            entry = {}
            if i.portal_type in items_with_bodytext:
                obj = i.getObject()
                entry['title'] = obj.Title()
                entry['desc'] = obj.Description()
                entry['text'] = obj.getText()
                entry['marker'] = 'collapse-%s' % counter
            else:
                info = u'<p>Für weitere Informationen klicken Sie bitte <a class="internal-link" href="%s">hier.</a></p>' %i.getURL() 
                entry['title'] = i.Title
                entry['desc'] = i.Description
                entry['text'] = info
                entry['marker'] = 'collapse-%s' % counter
            objectlist.append(entry)
            counter += 1
        self.objectlist = objectlist






