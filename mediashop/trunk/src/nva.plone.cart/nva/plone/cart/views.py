# -*- coding: utf-8 -*-

from five import grok

from zope.formlib import form
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.interfaces import IBelowContentBody

from nva.mediashop.interfaces import IOrderForm
from nva.plone.cart import utils, IPloneCart
from nva.cart import ICartAddable, ICartRetriever, ICartHandler


def null_validator(*args, **kwargs):
    """A validator that doesn't validate anything.
    
    This is somewhat lame, but if you have a "Cancel" type button that
    won't want to validate the form, you need something like this.

    @form.action(_(u"label_cancel", default=u"Cancel"),
                 validator=null_validator,
                 name=u'cancel')
    """
    return ()


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


class CartNamespace(object):
    """A mixin for changing the namespace of a view.
    """
    def update(self):
        self.portal_url = getToolByName(self.context, 'portal_url')()
    
    def default_namespace(self):
        namespace = grok.View.default_namespace(self)
        namespace['cart'] = self.context.cart
        namespace['is_member'] = self.context.is_member
        namespace['cart_url'] = self.portal_url + '/++cart++'
        namespace['handler'] = self.context.handler
        return namespace


class CartContent(CartNamespace, grok.View):
    grok.context(IPloneCart)
    

class CartView(CartNamespace, grok.View):
    """A view for the Plone cart
    """
    grok.name("summary")
    grok.context(IPloneCart)

    def update(self):
        CartNamespace.update(self)
        self.content = getMultiAdapter((self.context, self.request),
                                       name="cartcontent")()


class Checkout(CartNamespace, grok.Form):
    """A view for the Plone cart
    """
    grok.context(IPloneCart)
    label = "Bestellformular"
    form_name = "Bitte geben Sie alle Werte ein."
    form_fields = grok.Fields(IOrderForm)

    @form.action(u'Abbrechen', validator=null_validator)
    def handle_cancel(self, action, data):
        self.context.cart.clear()
        utils.flash(self.request, u"Der Bestellvorgang wurde abgebrochen.")
        self.request.response.redirect(self.portal_url)

    @form.action(u'Bestellen')
    def handle_order(self, action, data):
        print data, action

    def renderField(self, *args):
        label = required = description = error = input = "" 
        css_class = "field "
        for field in args:
            label += "%s " %field.label 
            if field.required:
                required = ('<span class="fieldRequired" title="Required"'
                            'tal:condition="plz/required">(Required)</span>')
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
