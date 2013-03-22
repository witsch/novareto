# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.bsbetreuung.wizard import delSbFromSession
from nva.bsbetreuung.interfaces import IProgress, IFinal
from nva.bsbetreuung import bsbetreuungMessageFactory as _


class Ibsb_finalView(Interface):
    """
    bsb_final view interface
    """
    def getFortsetzung():
        """
        Methode zur Ermittlung der Fortsetzung
        """

class bsb_finalView(BrowserView):
    """
    bsb_final browser view
    """
    implements(Ibsb_finalView, IProgress, IFinal)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getFortsetzung(self):
        """
        Methode zur Ermittlung der Fortsetzung
        """
        refs = self.context.getReferences()
        formaction = fortsetzung = self.context.id
        printurl = self.context.absolute_url() + '/bsbprint_view'
        if refs:
            fortsetzung = refs[0].absolute_url()
        if self.request.get('back', ''):
            return self.request.response.redirect(fortsetzung)
        if self.request.get('print', ''):
            return self.request.response.redirect(printurl)
        if self.request.get('erase', ''):
            delSbFromSession(self.context)
            url = self.context.aq_inner.aq_parent.absolute_url()
            return self.request.response.redirect(url)
        return formaction


