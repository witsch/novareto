# -*- coding: utf-8 -*-

from five import grok
from Acquisition import Explicit
from zope.component import adapts, getMultiAdapter
from zope.interface import Interface, implements, Attribute
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from nva.cart import ICartRetriever, ICartHandler


class IPloneCart(Interface):
    """A cart for Plone
    """
    cart = Attribute("The cart object")


class CartWrapper(Explicit):
    """A class that wraps a cart for acquisition (evil AQ !).
    """
    implements(IPloneCart)

    def __init__(self, parent, request, cart):
        self.cart = cart
        self.handler = ICartHandler(cart)
        self.request = request
        self.parent = parent

    def browserDefault(self, request):
        return self, ()

    def update(self):
        pass

    def render(self):
        view = getMultiAdapter((self, self.request), name="manage")
        return view.__call__()
    
    def __call__(self):
        self.update()
        return self.render()


class CartTraverser(grok.MultiAdapter):
    grok.name('cart')
    grok.implements(ITraversable)
    grok.adapts(Interface, IHTTPRequest)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        cart = ICartRetriever(self.request.SESSION)
        wrap = CartWrapper(self.context, self.request, cart)
        return wrap.__of__(self.context)
