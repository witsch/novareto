# -*- coding: utf-8 -*-
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.bsbetreuung.wizard import delSbFromSession
from nva.bsbetreuung.interfaces import IProgress
from nva.bsbetreuung import bsbetreuungMessageFactory as _


class Ibsb_startView(Interface):
    """
    bsb_start view interface
    """

    def getFortsetzung():
        """
        Methode zur Ermittlung der Fortsetzung
        """

class bsb_startView(BrowserView):
    """
    bsb_start browser view
    """
    implements(Ibsb_startView, IProgress)

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
        delSbFromSession(self.context)
        refs = self.context.getReferences()
        fortsetzung = None
        if refs:
            fortsetzung = refs[0].absolute_url()
        if self.request.get('weiter', ''):
            return self.request.response.redirect(fortsetzung)
        return fortsetzung

