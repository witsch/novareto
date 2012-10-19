# -*- coding: utf-8 -*- 

import os
import loremipsum
from random import randrange
import urllib2
from DateTime.DateTime import DateTime
from Products.Five.browser import BrowserView
from plone.namedfile import NamedImage
from plone.app.textfield.value import RichTextValue

def _invokeFactory(context, portal_type, id, **kw):
    context.invokeFactory(portal_type, id=id, **kw)
    obj = context[id]

    try:
        obj.portal_workflow.doActionFor(obj, 'publish')
    except:
        pass
    return obj

class Setup(BrowserView):

    def setupPFG(self, id_=None):
        """ Setup 'Bestellformular' as PFG instance """

        # fix allowed_content_types for FormFolder
        allowed = self.context.portal_types.FormFolder.allowed_content_types
        if not 'Dexterity Content Adapter' in allowed:
            self.context.portal_types.FormFolder.allowed_content_types = tuple(list(allowed) + ['Dexterity Content Adapter'])

        if id_ in self.context.objectIds():
            self.context.manage_delObjects(id_)

        form = _invokeFactory(self.context, 'FormFolder', id=id_, title='Bestellformular')
        form.manage_delObjects(['replyto', 'topic', 'comments'])
        form.setActionAdapter(['dexterity-adapter'])

        # content adapter
        adapter = _invokeFactory(form, 'Dexterity Content Adapter', id='dexterity-adapter', title='Dexterity Adapter')
        adapter.setCreatedType('nva.borrow.borrowrequest')
        adapter.setTargetFolder(self.context['bookings'])
        fields = ('unternehmen', 'mitgliedsnr', 'vorname', 'nachname', 'email', 
                  'telefon', 'fax', 'adresse', 'adresse2', 'plz', 'stadt', 'lieferzeit', 
                  'thema', 'besucherzahl', 'formData')
        mapping = [dict(form=f, content=f) for f in fields]
        adapter.setFieldMapping(mapping)

#        f = _invokeFactory(form, 'FormReadonlyStringField', id='buchungStart', title='Buchen von', required=True)
#        f.setFgTDefault('request/buchungStart|nothing')        
#        f = _invokeFactory(form, 'FormReadonlyStringField', id='buchungEnde', title='Buchen von', required=True)
#        f.setFgTDefault('request/buchungEnde|nothing')        
        f=_invokeFactory(form, 'FormRichLabelField', id='bestellung', title='Bestellte Aktionsmittel')
        f.setFgTDefault('object/showBestellung | nothing')        

        _invokeFactory(form, 'FormStringField', id='unternehmen', title='Unternehmen', required=True)
        _invokeFactory(form, 'FormStringField', id='mitgliedsnr', title='Mitgliedsnummer bei BGETEM', required=True)
        _invokeFactory(form, 'FormStringField', id='vorname', title='Vorname (Ansprechpartner)', required=True)
        _invokeFactory(form, 'FormStringField', id='nachname', title='Nachname (Ansprechpartner)', required=True)
        _invokeFactory(form, 'FormStringField', id='email', title='E-Mail Adresse (Ansprechpartner)', required=True)
        _invokeFactory(form, 'FormStringField', id='telefon', title='Telefon (Ansprechpartner)', required=True)
        _invokeFactory(form, 'FormStringField', id='fax', title='Fax (Ansprechpartner)')

        _invokeFactory(form, 'FormStringField', id='adresse', title='Lieferaddresse (keine Postfach)', required=True)
        _invokeFactory(form, 'FormStringField', id='adresse2', title='Adresszusatz (Gebäude, Einfahrt, Tor usw.)', required=False)
        _invokeFactory(form, 'FormStringField', id='plz', title='Postleitzahl', required=True)
        _invokeFactory(form, 'FormStringField', id='stadt', title='Stadt', required=True)
        _invokeFactory(form, 'FormStringField', id='lieferzeit', title='Lieferzeit/Bürozeit (wann ist jemand zu Haus)', required=True)
        _invokeFactory(form, 'FormStringField', id='thema', title='Thema Aktionstag', required=False)
        _invokeFactory(form, 'FormStringField', id='besucherzahl', title='Erwartete Besucherzahl', required=False)
        
        f = _invokeFactory(form, 'FormReadonlyStringField', id='formData', title='formData', required=True)
        f.setHidden(True)
        f.setFgTDefault('request/formData|nothing')        


    def createBookingRequest(self, intid=None):
        form_folder = self.context.portal_catalog(portal_type='FormFolder')[0].getObject()
        self.request.response.redirect(form_folder.absolute_url() + '?intid=%s' % intid)

    def getIntId(self):
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds
        return getUtility(IIntIds).getId(self.context)
