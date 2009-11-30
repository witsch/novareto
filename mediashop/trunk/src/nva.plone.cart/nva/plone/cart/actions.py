# -*- coding: utf-8 -*-

from five import grok
from nva.cart import IDiscountedCartItem
from nva.plone.cart import utils, ISessionCart, IMemberCart
from zope.interface import directlyProvides, noLongerProvides
from zope.publisher.interfaces import NotFound
from Products.CMFCore.utils import getToolByName


class CartItemMember(grok.View):
    grok.name("membership")
    grok.context(ISessionCart)

    def update(self):
        if IMemberCart.providedBy(self.context.cart):
            noLongerProvides(self.context.cart, IMemberCart)
            for item in self.context.cart.values():
                noLongerProvides(item, IDiscountedCartItem)
        else:
            directlyProvides(self.context.cart, IMemberCart)
            for item in self.context.cart.values():
                item.discount_factor = 0.5
                item.discount = u"Membership"
                directlyProvides(item, IDiscountedCartItem)            
            
    def render(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/++cart++/summary")


class CartItemDelete(grok.View):
    grok.name("delete")
    grok.context(ISessionCart)

    def render(self):
        return u"Product code missing."

    def publishTraverse(self, request, name):
        result = self.context.handler.delItem(name)
        if not result:
            raise NotFound(self, name, request)
        else:
            utils.flash(self.request, u"Item %r removed from cart." % name)

        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/++cart++/summary")


class CartItemPlus(grok.View):
    grok.name("plus")
    grok.context(ISessionCart)

    def render(self):
        return u"Product code missing."

    def publishTraverse(self, request, name):
        item = self.context.handler.getItem(name)
        if not item:
            raise NotFound(self, name, request)
        else:
            item.quantity += 1
            utils.flash(self.request, u"Quantity increased for item %r." % name)

        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/++cart++/summary")


class CartItemMinus(grok.View):
    grok.name("minus")
    grok.context(ISessionCart)

    def render(self):
        return u"Product code missing."

    def publishTraverse(self, request, name):
        item = self.context.handler.getItem(name)
        if not item:
            raise NotFound(self, name, request)
        else:
            if item.quantity <= 1:
                status = u"Deleted item %r."
                self.context.handler.delItem(name)
            else:
                status = u"Quantity decreased for item %r."
                item.quantity -= 1

        utils.flash(self.request, status % name)
        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/++cart++/summary")