from five import grok

from Acquisition import Explicit
from zope.publisher.interfaces import NotFound

from zope.component import adapts, getMultiAdapter
from zope.interface import Interface, implements, Attribute
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from nva.cart import ICartAddable, ICartRetriever, ICartHandler

from plone.app.layout.viewlets.interfaces import IBelowContentBody
from nva.mediashop.interfaces import IOrderForm
from zope.formlib import form
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName


def null_validator(*args, **kwargs):
    """A validator that doesn't validate anything.
    
    This is somewhat lame, but if you have a "Cancel" type button that
    won't want to validate the form, you need something like this.

    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    """
    return ()


class IPloneCart(Interface):
    """A cart for Plone
    """
    cart = Attribute("The cart object")


class AddToCartLink(grok.Viewlet):
    grok.viewletmanager(IBelowContentBody)
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


class Checkout(grok.Form):
    """A view for the Plone cart
    """
    grok.context(IPloneCart)
    lable="Bestellformular"
    form_name="Bitte geben Sie alle Werte ein."
    form_fields = grok.Fields(IOrderForm)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @form.action(u'Abbrechen', validator=null_validator)
    def handle_cancel(self, action, data):
        self.context.cart.clear()
        view_url = self.portal.absolute_url()
        IStatusMessage(self.request).addStatusMessage("Der Bestellvorgang wurde abgebrochen.", type='info')
        self.request.response.redirect(view_url)


    @form.action(u'Bestellen')
    def handle_order(self, action, data):
        print data, action

    def renderField(self, *args):
        label = required = description = error = input = "" 
        css_class = "field "
        for field in args:
            label += "%s " %field.label 
            if field.required:
                required ='<span class="fieldRequired" title="Required" tal:condition="plz/required"> (Required) </span>'
            if field.hint:
                description += "%s " % field.hint
            if field.error():
                error += "%s " %field.error()
            input += "%s " %field()    
            id = field.name.replace('.', '_')
            css_class += "%s_" %field.name
        if len(error.strip()) > 0:
            css_class = css_class + ' error'
        ret = """
        <div id="%s" class="%s">
           <label> %s </label>
           %s
           <div class="formHelp">%s</div>
           <div class="fieldErrorBox"> %s </div>
           <span class="widget"> %s </span>
        </div>""" %(id, css_class, label, required, description, error, input)
        return ret 

    def default_namespace(self):
        namespace = grok.View.default_namespace(self)
        namespace['cart'] = self.context.cart
        namespace['handler'] = ICartHandler(self.context.cart)
        namespace['context'] = self.context.parent
        namespace['here'] = self.context.parent
        return namespace


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
