# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface, Attribute
from zope.container.interfaces import IContainer
from zope.container.constraints import contains
from nva.cart import cartFactory as _


class ICartAddable(Interface):
    """Marker interface for objects that can be added to an ICart.
    """


class IDiscountedCartItem(Interface):
    """A discounted item.
    """
    discount = Attribute('Reason of the discount')

    discount_factor = schema.Float(
        default = 0.5,
        required = True,
        title = _(u"Discount percentage")
        )
    
    discount_price = schema.Float(
        default = 0.0,
        required = True,
        title = _(u"Price for a unit")
        )


class ICartItem(Interface):
    """A cart item.
    """
    title = schema.TextLine(
        required = True,
        title = _(u"Descritive name of the product")
        )
    
    code = schema.ASCIILine(
        required = True,
        title = _(u"Unique code of the product")
        )
    
    price = schema.Float(
        default = 0.0,
        required = True,
        title = _(u"Price for a unit")
        )

    url = schema.URI(
        required = False,
        title = _(u"URL to the product's sheet")
        )

    quantity = schema.Int(
        default = 1,
        required = True,
        title = _(u"Number of unit")
        )

    max_quantity = schema.Int(
        required = True,
        title = _(u"Maximum number of orderable items.")
        )

    weight = schema.Float(
        required = False,
        title = _(u"Weight of the product"),
        )

    total_price = Attribute("Computed attribute.")


class ICart(IContainer):
    """A cart containing items, ready for a checkout.
    """
    contains(ICartItem)


class ICartHandler(Interface):
    """A component destined to handle the basic cart's operations.
    """
    cart = schema.Object(
        title = u"The cart",
        schema = ICart,
        required = True
        )
    
    def addItem(item):
        """Adds an ICartAddable object to the cart.
        """

    def getItem(code):
        """Returns a ICartItem object.
        """

    def getItems():
        """Returns a list of ICartItem objects.
        """

    def getTotalPrice():
        """Returns the total price
        """

    def clear():
        """Clears the cart.
        """


class ICartRetriever(Interface):
    """A component dedicated in retrieving a cart.
    """
