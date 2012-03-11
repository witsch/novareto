# -*- coding: utf-8 -*-

from five import grok
from nva.cart import Cart, ICartRetriever
from Products.Transience.TransientObject import TransientObject

from zope.publisher.interfaces.http import IHTTPRequest
from collective.beaker.interfaces import ISession


@grok.adapter(IHTTPRequest)
@grok.implementer(ICartRetriever)
def session_cart_retriever(request):
    """Get the current cart.
    """
    session = ISession(request)
    session = request.SESSION
    cart = session.get('nva.cart', None)
    print session, cart
    if cart is None:
        cart = session['nva.cart'] = Cart()
    return cart
