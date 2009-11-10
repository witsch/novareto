# -*- coding: utf-8 -*-

from nva.cart import ICartItem
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty


class CartItem(object):
    """A base cart item.
    """
    implements(ICartItem)
    
    title = FieldProperty(ICartItem["title"])
    url = FieldProperty(ICartItem["url"])
    code = FieldProperty(ICartItem["code"])
    price = FieldProperty(ICartItem["price"])
    weight = FieldProperty(ICartItem["weight"])
    quantity = FieldProperty(ICartItem["quantity"])

    @property
    def total_price(self):
        """A base implementation of the total price.
        It does not take the weight in account.
        """
        return self.quantity * self.price
