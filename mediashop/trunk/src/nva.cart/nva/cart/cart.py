# -*- coding: utf-8 -*-

from BTrees import OOBTree
from nva.cart.interfaces import *
from zope.component import adapts
from zope.interface import implements


class Cart(OOBTree.OOBTree):
    """The cart.
    """
    implements(ICart)


class CartHandler(object):
    """CRUD operation on an ICart
    """
    adapts(ICart)
    implements(ICartHandler)

    def __init__(self, cart):
        self.cart = cart
        self.__member__ =  True

    def addItem(self, item):
        if not ICartAddable.providedBy(item):
            raise ValueError("%r does not provide %r" % (item, ICartAddable))

        # Fails if not adaptable. On purpose.
        cart_item = ICartItem(item)
        code = cart_item.code
        
        if code in self.cart:
            cart_item = self.cart[code]
            cart_item.quantity += 1

        self.cart[code] = cart_item

    def getItem(self, code):
        return self.cart.get(code)

    def getItems(self):
        for value in self.cart.values():
            if ICartItem.providedBy(value):
                yield value

    def delItem(self, code):
        if code in self.cart:
            del self.cart[code]
            return True
        return False

    def getTotalPrice(self):
        price = 0.0
        for item in self.getItems():
            price += item.portlet_total_price
        return price

    def getMemberPrice(self):
        price = 0.0
        for item in self.getItems():
            price += item.portlet_member_price 
        return price

    def clear(self):
        self.cart.clear()
