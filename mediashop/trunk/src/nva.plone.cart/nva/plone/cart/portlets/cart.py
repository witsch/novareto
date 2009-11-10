# -*- coding: utf-8 -*-

from five import grok
from zope.interface import implements, Interface
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.cachedescriptors.property import CachedProperty

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from nva.cart import Cart, ICartAddable, ICartRetriever, ICartHandler

_ = MessageFactory('nva.plone.cart')


class ICartPortlet(IPortletDataProvider):
    pass


class Assignment(base.Assignment):
    implements(ICartPortlet)

    @property
    def title(self):
        return _(u"Shopping Cart")


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/cart.pt')

    @CachedProperty
    def cart(self):
        return ICartRetriever(self.request.SESSION)

    def update(self):
        self.portal = self.context.portal_url()
        self.url = self.context.absolute_url()
        self.handler = ICartHandler(self.cart)

    @property
    def available(self):
        return bool(len(self.cart))
