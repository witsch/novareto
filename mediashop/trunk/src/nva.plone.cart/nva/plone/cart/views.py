from five import grok

from Acquisition import Explicit
from zope.publisher.interfaces import NotFound

from zope.component import adapts, getMultiAdapter
from zope.interface import Interface, implements, Attribute
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from nva.cart import ICartAddable, ICartRetriever, ICartHandler

from plone.app.layout.viewlets.interfaces import IAboveContent


class IPloneCart(Interface):
    """A cart for Plone
    """
    cart = Attribute("The cart object")


class AddToCartLink(grok.Viewlet):
    grok.viewletmanager(IAboveContent)
    grok.context(ICartAddable)


class AddToCart(grok.View):
    """Add an item to the cart
    """
    grok.name('cart.add')
    grok.context(ICartAddable)

    def update(self):
        self.cart = ICartRetriever(self.request.SESSION)

    def render(self):
        handler = ICartHandler(self.cart)
        handler.addItem(self.context)
        self.redirect(self.url(self.context))


class Checkout(grok.View):
    """A view for the Plone cart
    """
    grok.context(IPloneCart)

    def render(self):
        return u"Here should be the checkout form."


class CartView(grok.View):
    """A view for the Plone cart
    """
    grok.name("manage")
    grok.context(IPloneCart)
 
    def default_namespace(self):
        namespace = grok.View.default_namespace(self)
        namespace['cart'] = self.context.cart
        namespace['handler'] = ICartHandler(self.context.cart)
        namespace['context'] = self.context.parent
        namespace['here'] = self.context.parent
        return namespace


class CartWrapper(Explicit):
    """A class that wraps a cart for acquisition (evil AQ !).
    """
    implements(IPloneCart)

    def __init__(self, parent, request, cart):
        self.cart = cart
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
