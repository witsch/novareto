# -*- coding: utf-8 -*-
from plone.app.portlets.portlets.navigation import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyNavRenderer(Renderer):

    def render(self):
        """ Es soll lediglich das eigene Template genutzt werden. """

        return self._template()

    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')
