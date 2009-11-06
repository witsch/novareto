# -*- coding: utf-8 -*-

from five import grok
from nva.cart import Cart, ICartRetriever
from Products.Transience.TransientObject import TransientObject


@grok.adapter(TransientObject)
@grok.implementer(ICartRetriever)
def session_cart_retriever(session):
    """Get the current cart.
    """
    cart = session.get('nva.cart', None)
    if cart is None:
        cart = session['nva.cart'] = Cart()
    return cart
