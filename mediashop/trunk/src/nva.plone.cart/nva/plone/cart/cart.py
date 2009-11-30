# -*- coding: utf-8 -*-

from five import grok
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.PortalFolder import PortalFolderBase

from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from plone.app.content.item import Item
from plone.app.content.container import Container

from nva.cart import ICartRetriever, ICartHandler
from nva.plone.cart.interfaces import IOrderFolder, IOrder
from nva.plone.cart.interfaces import ISessionCart, ICartWrapper, IMemberCart


class OrderFolder(Container):
    """A Cart folder implementation.
    """
    implements(IOrderFolder)
    meta_type = portal_type = 'OrderFolder'
    manage_options = PortalFolderBase.manage_options

    def __setitem__(self, name, obj):
        name = name.encode('ascii') # may raise if there's a bugus id
        self._setObject(name, obj, set_owner=0)


class CartMixin(Item):
    """A cart wrapper that takes care of all the non-core accesses.
    """
    implements(ICartWrapper)

    def __init__(self, cart, id="++cart++"):
        Item.__init__(self, id=id)
        self.cart = cart
        self.id = id
    
    def browserDefault(self, request):
        view = getMultiAdapter((self, request), name="summary")
        return view, ()


class SessionCart(CartMixin):
    """A cart living in the session.
    """
    implements(ISessionCart)
    meta_type = portal_type = 'TempFolder'
    Title = getTitle = lambda self:u"Cart"

    @property
    def is_member(self):
        return not IMemberCart.providedBy(self.cart)

    @property
    def handler(self):
        return ICartHandler(self.cart)


class Order(CartMixin):
    """A persisted cart.
    """
    implements(IOrder)
    meta_type = portal_type = 'Order'
    Title = getTitle = lambda self:u"Order %s" % self.id
    manage_options = PortalFolderBase.manage_options

    is_member = True 

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
