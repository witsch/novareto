# -*- coding: utf-8 -*-
from plone.app.portlets.portlets.navigation import Renderer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish

class MyNavRenderer(Renderer):

    @property
    def isportalcontext(self):
        """ Diese Funktion liefert einen Boolwert zurück der aussagt,
            ob wir im direkten Context des Portals stehen. In diesem
            Fall soll der Backlink nicht angeboten werden. """
        context = self.context.aq_inner
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        if context == portal:
            return True
        if not IFolderish.providedBy(context):
            if context.aq_parent == portal:
                return True
        return False

    @property
    def isdefaultpage(self):
        """ Diese Funktion liefert einen Boolwert zurück der aussagt,
            ob es sich beim Context um die Standardansicht eines Ordners
            handelt. """
        context = self.context.aq_inner
        if not IFolderish.providedBy(context) or context.portal_type == 'Topic':
            if hasattr(context.aq_parent, 'default_page'):
                if context.id == context.aq_parent.default_page:
                    return True
        return False        


    def render(self):
        """ Ueberschreibt den Standard-Renderer fuer das Navigations-
            portlet. Im Kopf des Navigationsportlets soll ein Zurueck-
            link angezeigt werden damit vor allem im mobilen Bereich
            eine Off-Canvas zurueck Navigation erreicht werden kann. """

        back = self.context.aq_inner.aq_parent
        context = self.context.aq_inner

        self.heading_link_target = ""

        #In der Wurzel des Plone-Portals soll kein Backlink erscheinen
        if self.isportalcontext:
            self.back_name = ''
            self.back_url = ''
            return self._template()

        self.back_name = back.title
        self.back_url = back.absolute_url()
        #Sonderfall-1: Folderview in der 1. Ebene, zurueck zur Startseite
        if IFolderish.providedBy(context):
            if back.portal_type == 'Plone Site':
                self.back_name = u'Startseite'
                return self._template()
        
        #Sonderfall-2: Pruefung, ob es sich beim Contextobjekt um eine Standard-
        #              ansicht eines Ordners handelt.
        if self.isdefaultpage:
            #Variante-2a: Contextobjekt ist Standardansicht bei einem Ordner der 1. Ebene.
            if back.aq_parent.portal_type == 'Plone Site':
                self.back_name = 'Startseite'
                self.back_url = back.aq_parent.absolute_url()
            #Variante-2b: Contextobjekt ist Standardansicht eines Ordners beliebiger Ebene.   
            else:
                self.back_name = back.aq_parent.title
                self.back_url = back.aq_parent.absolute_url()
        return self._template()

    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')
