# -*- coding: utf-8 -*-

from five import grok
from OFS.SimpleItem import SimpleItem
from BTrees.OOBTree import OOBTree
from Acquisition import Explicit, aq_inner
from zope.schema import Bool
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable
from zope.component import adapts, getMultiAdapter
from zope.interface import Interface, implements, Attribute, directlyProvides
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable
from nva.cart import ICartRetriever, ICartHandler


class IPloneCart(Interface):
    """A cart for Plone
    """
    cart = Attribute("The cart object")
    is_member = Bool(title=u"I am a member")


class CartWrapper(SimpleItem):
    """A class that wraps a cart for acquisition (evil AQ !).
    """
    implements(IPloneCart)
    id = "++cart++"

    Title = getTitle = lambda self:u"Cart"

    @apply
    def is_member():
        def set(self, value):
            self.properties['is_member'] = value
        def get(self):
            return self.properties.get('is_member', False)
        return property(get, set)

    def cart_properties(self):
        annotation = IAnnotations(self.cart)
        properties = annotation.get('nva.plone.cart')
        if not properties:
            properties = annotation['nva.plone.cart'] = OOBTree()
        return properties

    def __init__(self, parent, request, cart):
        if not IAttributeAnnotatable.providedBy(cart):
            directlyProvides(cart, IAttributeAnnotatable)
        self.cart = cart
        self.handler = ICartHandler(cart)
        self.request = request
        self.parent = parent
        self.properties = self.cart_properties()

    def browserDefault(self, request):
        view = getMultiAdapter((self, self.request), name="summary")
        return view, ()


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
