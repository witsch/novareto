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
        if self.context._member is True:
            self.context._member = False
            for item in self.context.cart.values():
                if item == True or item == False:
                    print "??"
                else:
                    noLongerProvides(item, IDiscountedCartItem)
        else:
            self.context._member = True
            for item in self.context.cart.values():
                if item == True or item == False:
                    print "??"
                else:
                    directlyProvides(item, IDiscountedCartItem)
            
    def render(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/medienangebot/medienshop/++cart++/summary")


class CheckoutMembership(grok.View):
    grok.name('membership_final')
    grok.context(ISessionCart)
   
    def fF(self, value):
        return "%.2f" %float(value)
 
    def render(self):
        if self.context._member is True:
            self.context._member = False
            price = self.context.handler.getMemberPrice()
        else:
            self.context._member = True
            price = self.context.handler.getTotalPrice()
        price = self.fF(price)
        return "[{'membership': %s, 'price': '%s'}]" % (
            str(self.context._member).lower(), str(price))


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
        self.redirect(portal_url + "/medienangebot/medienshop/++cart++/summary")
        

class CartAction(grok.View):
    grok.baseclass()
    grok.context(ISessionCart)

    def render(self):
        return u"Product code missing."

    def getItem(self, name):
        item = self.context.handler.getItem(name)
        if not item:
            raise NotFound(self, name, self.request)
        return item


class CartItemPlus(CartAction):
    grok.name("plus")

    def publishTraverse(self, request, name):
        item = self.getItem(name)
        if item.quantity < item.max_quantity:
            item.quantity += 1
            status = u"Quantity increased for item %r."
        else:
            status = u"Reached max quantity for item %r."
            
        utils.flash(self.request, status % name)
        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/medienangebot/medienshop/++cart++/summary")


class CartItemMinus(CartAction):
    grok.name("minus")

    def publishTraverse(self, request, name):
        item = self.getItem(name)
        item = self.context.handler.getItem(name)
        if item.quantity <= 1:
            status = u"Deleted item %r."
            self.context.handler.delItem(name)
        else:
            status = u"Quantity decreased for item %r."
            item.quantity -= 1

        utils.flash(self.request, status % name)
        portal_url = getToolByName(self.context, 'portal_url')()
        self.redirect(portal_url + "/medienangebot/medienshop/++cart++/summary")
