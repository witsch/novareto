# -*- coding: utf-8 -*-

from five import grok
from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem

from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from plone.app.content.container import Container

from nva.cart import ICartRetriever, ICartHandler
from nva.plone.cart.interfaces import IOrderFolder, IOrder
from nva.plone.cart.interfaces import ISessionCart, ICartWrapper


class OrderFolder(Container):
    """A Cart folder implementation.
    """
    implements(IOrderFolder)
    meta_type = portal_type = 'OrderFolder'

    def __setitem__(self, name, obj):
        name = name.encode('ascii') # may raise if there's a bugus id
        self._setObject(name, obj, set_owner=0)


class CartMixin(SimpleItem, OOBTree):
    """A cart wrapper that takes care of all the non-core accesses.
    """
    implements(ICartWrapper)
    
    def __init__(self, cart, id="++cart++", is_member=False):
        SimpleItem.__init__(self, id=id)
        OOBTree.__init__(self)
        self['cart'] = cart
        self['is_member'] = is_member
        self.id = id

    def browserDefault(self, request):
        view = getMultiAdapter((self, request), name="summary")
        return view, ()


class SessionCart(CartMixin):
    """A cart living in the session.
    """
    implements(ISessionCart)
    Title = getTitle = lambda self:u"Cart"

    @property
    def handler(self):
        return ICartHandler(self['cart'])


class Order(CartMixin):
    """A persisted cart.
    """
    implements(IOrder)
    meta_type = portal_type = 'Order'
    Title = getTitle = lambda self:u"Order %s" % self.id

    @property
    def reference(self):
        return self.id


class CartTraverser(grok.MultiAdapter):
    grok.name('cart')
    grok.implements(ITraversable)
    grok.adapts(Interface, IHTTPRequest)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        cart = ICartRetriever(self.request.SESSION)
        return SessionCart(cart).__of__(self.context)
