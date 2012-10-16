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

        # content adapter
        adapter = _invokeFactory(form, 'Dexterity Content Adapter', id='dexterity-adapter', title='Dexterity Adapter')
        adapter.setCreatedType('nva.borrow.borrowrequest')
#        adapter.setTargetFolder('bookings')
        adapter.setFieldMapping([dict(form='vorname', content='firstName'),
                                 dict(form='nachname', content='lastName'),
                                 dict(form='adresse', content='address'),
                                 dict(form='plz', content='zip'),
                                 dict(form='stadt', content='city'),
                                 dict(form='telefon', content='phone'),
                                 dict(form='email', content='email'),
                                 dict(form='buchungStart', content='borrowFrom'),
                                 dict(form='buchungEnde', content='borrowTo'),
                                 dict(form='kommentar', content='comment'),
            ])

        _invokeFactory(form, 'FormStringField', id='vorname', title='Vorname', required=True)
        _invokeFactory(form, 'FormStringField', id='nachname', title='Nachname', required=True)
        _invokeFactory(form, 'FormStringField', id='adresse', title='Adresse', required=True)
        _invokeFactory(form, 'FormStringField', id='plz', title='Postleitzahl', required=True)
        _invokeFactory(form, 'FormStringField', id='stadt', title='Stadt', required=True)
        _invokeFactory(form, 'FormStringField', id='telefon', title='Telefon')
        _invokeFactory(form, 'FormStringField', id='email', title='E-Mail Adresse')
        _invokeFactory(form, 'FormStringField', id='mitgliedsnr', title='Mitgliedsnummer', required=True)

        _invokeFactory(form, 'FormDateField', id='buchungStart', title='Buchen von', required=True)
        _invokeFactory(form, 'FormDateField', id='buchungEnde', title='Buchen bis', required=True)
        _invokeFactory(form, 'FormTextField', id='kommentar', title='Kommentar')

        self.request.response.redirect(form.absolute_url())

    def createBookingRequest(self, intid=None):
        form_folder = self.context.portal_catalog(portal_type='FormFolder')[0].getObject()
        self.request.response.redirect(form_folder.absolute_url() + '?intid=%s' % intid)

    def getIntId(self):
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds
        return getUtility(IIntIds).getId(self.context)
