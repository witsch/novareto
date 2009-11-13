# -*- coding: utf-8 -*-

from zope.schema import Object, TextLine, Float, Bool
from zope.interface import Interface, Attribute
from zope.app.container.constraints import contains
from nva.cart import ICartHandler


class ICartWrapper(Interface):
    """An object that wraps a cart.
    """
    is_member = Bool(
        title = u"The cart owner is a member",
        default = False
        )

    def __init__(cart, *arg, **kw):
        """Initialize the cart wrapper.
        """


class ISessionCart(ICartWrapper):
    """A cart for Plone
    """        
    handler = Object(
        title = u"Cart controler allowing CRUD operations",
        schema = ICartHandler,
        readonly = True
        )


class IOrder(ICartWrapper):
    """A cart that has been checked out.
    """
    reference = TextLine(
        title = u"Reference of the order",
        readonly = True
        )

    total_price = Float(
        title = u"Pinned price of the order.",
        )


class IOrderFolder(Interface):
    """A folder containing orders.
    """
    contains(IOrder)
