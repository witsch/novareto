# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from nva.onlinetest.lib.services import getRegistrierdaten, getErgebnisdaten
from nva.flgcert.app import checkSuccess, checkStatus, checkCertificate
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from nva.portlet.flgstatus import FlgStatusPortletMessageFactory as _


class IFlgStatusPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    titel = schema.TextLine(title=_(u"Titel"),
                                  description=_(u"Bitte geben Sie hier den Titel des Portlets an."),
                                  required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFlgStatusPortlet)

    titel = u"Ihr Fortschritt"

    def __init__(self, titel=u""):
        self.titel = titel

    @property
    def title(self):
        """This property is used to give the titel of the portlet in the
        "manage portlets" screen.
        """
        return "FLG Status Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('flgstatusportlet.pt')

    def getStatusImage(self, status):
        images = {0:'flg_fortschritt_0.png',
                  1:'flg_fortschritt_12-5.png',
                  2:'flg_fortschritt_25.png',
                  3:'flg_fortschritt_37-5.png',
                  4:'flg_fortschritt_50.png',
                  5:'flg_fortschritt_62-5.png',
                  6:'flg_fortschritt_75.png',
                  7:'flg_fortschritt_87-5.png',
                  8:'flg_fortschritt_100.png',
                  }
        url = ''
        pcat = getToolByName(self.context, 'portal_catalog')
        brain = pcat.searchResults(id = images.get(status))
        if brain:
            url = brain[0].getURL()
        return url

    def getStatusSymbolUrl(self, cert):
        abschluss = {'cert':('bescheinigung.png', 'printcertificate'),
                     'seminar':('seminar.png', 'seminar'),
                     'talk':('gespraech.png', 'talk'),
                    }
        imageurl = ''
        pcat = getToolByName(self.context, 'portal_catalog')
        brain = pcat.searchResults(id = abschluss.get(cert)[0])
        if brain:
            imageurl = brain[0].getURL()
        return imageurl, abschluss.get(cert)[1]

    def getUserData(self):
        pm = getToolByName(self.context, 'portal_membership')
        id = pm.getAuthenticatedMember().getId()
        flg_id = self.context.getServiceid()
        reg = getRegistrierdaten(id, flg_id)
        erg = getErgebnisdaten(id, flg_id)
        success = checkSuccess(erg)
        status = checkStatus(erg)
        cert = checkCertificate(reg)
        return (success, status, cert)

    def getResults(self):
        data = self.getUserData()
        print data
        statusimage = self.getStatusImage(data[1])
        abschlussimage = ''
        abschlussurl = ''
        if data[0] == 1:
            print 'getSymbolUrl'
            abschluss = self.getStatusSymbolUrl(data[2])
            print abschluss
            abschlussimage = abschluss[0]
            abschlussurl = abschluss[1]
        if data[0] == -1:
            abschlussimage = ''
            abschlussurl = 'nocertificate'
        results = {'titel':self.data.titel,
                   'success':data[0],
                   'statusimage' : statusimage,
                   'abschlussimage' : abschlussimage,
                   'abschlussurl' : abschlussurl}
        return results
        

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IFlgStatusPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFlgStatusPortlet)
