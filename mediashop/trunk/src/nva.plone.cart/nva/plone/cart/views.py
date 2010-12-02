# -*- coding: utf-8 -*-

import copy
import datetime
from five import grok
from Acquisition import aq_base

import uuid
from zope.formlib import form
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.interfaces import IBelowContentBody
from Products.CMFPlone.utils import _createObjectByType

from nva.mediashop.interfaces import IOrderForm
from nva.mediashop.content import ShippingInformation
from nva.cart import ICartAddable, ICartRetriever, ICartHandler
from nva.cart import IDiscountedCartItem

from nva.plone.cart import utils
from nva.plone.cart import ISessionCart
from nva.plone.cart import IOrder, IOrderFolder, OrderFolder, Order

from nva.plone.cart import ploneCartFactory as _

from zope.app.form.interfaces import WidgetInputError
from zope.formlib.form import setUpWidgets
from zope.app.form.browser.boolwidgets import CheckBoxWidget
from zope.event import notify
from zope.app.container.contained import ObjectAddedEvent

ORDERS = "orders"
TEMPORDERS = "temp_print"


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

    def update(self, redirect=0):
        self.cart = ICartRetriever(self.request)
        self.redirect = redirect

    def render(self):
        quantity = 0
        handler = ICartHandler(self.cart)
        max_quantity = self.context.quantity
        buyablecontentadapter = handler.getItem(self.context.code)
        if buyablecontentadapter:
            quantity = buyablecontentadapter.quantity
        if quantity < max_quantity:
            handler.addItem(self.context)
        else:    
            utils.flash(self.request, _(u"Der maximale Bestellmenge dieses Artikel ist erreicht."))
        url = self.url(self.context)    
        if self.redirect == '0':
            url = self.url(self.context.aq_inner.aq_parent)
        elif self.redirect == '2':
            url = self.url(self.context.aq_inner.aq_parent.aq_parent, 'all')
        self.request.response.redirect(url)


class CartNamespace(object):
    """A mixin for changing the namespace of a view.
    """
    def update(self):
        self.portal_url = getToolByName(self.context, 'portal_url')()
    
    def default_namespace(self):
        namespace = grok.View.default_namespace(self)
        namespace['cart'] = self.context.cart
        namespace['cart_url'] = self.portal_url + '/medien/medienkatalog/++cart++'
        namespace['handler'] = self.context.handler
        return namespace


class CartContent(CartNamespace, grok.View):
    grok.context(ISessionCart)


class OrderFolderView(grok.View):
    grok.name("summary")
    grok.context(IOrderFolder)

    def orders(self):
        for order in self.context.values():
            yield {
                'ref': order.reference,
                'date': order.CreationDate(),
                'len': len(order.cart),
                'price': order.total_price,
                'is_member': order.is_member
                }


class OrderView(grok.View):
    grok.name("summary")
    grok.context(IOrder)

    def update(self):
        self.ordered_items = self.context.cart.values()
        self.total_price = self.context.total_price
        self.is_member = self.context.is_member
        self.date = self.context.CreationDate()
        

class CartView(CartNamespace, grok.View):
    """A view for the Plone cart
    """
    grok.name("summary")
    grok.context(ISessionCart)

    def update(self):
        CartNamespace.update(self)
        self.content = getMultiAdapter((self.context, self.request),
                                       name="cartcontent")()



class Checkout(CartNamespace, grok.Form):
    """A view for the Plone cart
    """
    grok.context(ISessionCart)
    label = _(u"Bestellformular")
    form_name = _(u"Bitte geben Sie alle Werte ein.")
    form_fields = grok.Fields(IOrderForm)
    form_fields['datenschutz'].custom_widget = CheckBoxWidget
    form_fields['lieferadresse'].custom_widget = CheckBoxWidget 

    def validate_checkout(self, action, data):
        errors = self.validate(action, data)
        err = None 
        if data.get('datenschutz') == False:
            datenschutz = self.widgets.get('datenschutz')
            datenschutz._error = err = WidgetInputError(field_name='datenschutz',
                                           widget_title=u'Datenschutz', 
                                           errors=_(u'Bitte das Feld Datenschutzvereinbarung bestätigen.'))
            errors.append(err) 
        
        if not self.context.is_member and data.get('mitgliedsnummer') == None:
            mnr = self.widgets.get('mitgliedsnummer')
            mnr._error = err = WidgetInputError(field_name='mitgliedsnummer',
                                                widget_title=u'Mitgliedsnummer', 
                                                errors=_(u'Bitte Mitgliedsnummer prüfen'))
            errors.append(err) 

        if data.get('lieferadresse'):

            lfirma = data.get('lfirma')
            if not lfirma:
		field = self.widgets.get('lfirma')
		field._error = err = WidgetInputError(field_name='Firma',
							widget_title=u'Firma', 
							errors=_(u'Bitte dieses Feld bearbeiten.'))
		errors.append(err) 

            lname = data.get('lname')
            if not lname:
		field = self.widgets.get('lname')
		field._error = err = WidgetInputError(field_name='Name',
							widget_title=u'Name', 
							errors=_(u'Bitte dieses Feld bearbeiten.'))
		errors.append(err) 

            lstrasse = data.get('lstrasse')
            if not lstrasse:
		field = self.widgets.get('lstrasse')
		field._error = err = WidgetInputError(field_name='Strasse',
							widget_title=u'Strasse', 
							errors=_(u'Bitte dieses Feld bearbeiten.'))
		errors.append(err) 

            lplz = data.get('lplz')
            if not lplz:
		field = self.widgets.get('lplz')
		field._error = err = WidgetInputError(field_name='Postleitzahl',
							widget_title=u'Postleitzahl', 
							errors=_(u'Bitte dieses Feld bearbeiten.'))
		errors.append(err) 

            lort = data.get('lort')
            if not lort:
		field = self.widgets.get('lort')
		field._error = err = WidgetInputError(field_name='Ort',
							widget_title=u'Ort', 
							errors=_(u'Bitte dieses Feld bearbeiten.'))
		errors.append(err) 
        return errors    

    def setUpWidgets(self, ignore_request=False):
        super(Checkout, self).setUpWidgets(ignore_request=ignore_request)
        self.widgets['plz'].displayWidth = 5 
        self.widgets['lplz'].displayWidth = 5 

    @form.action(_(u'Zurück zum Warenkorb'), validator=null_validator)
    def handle_cancel(self, action, data):
        self.request.response.redirect(self.portal_url+'/medien/medienkatalog/++cart++')

    @form.action(_(u'Abbrechen'), validator=null_validator)
    def handle_cancel(self, action, data):
        self.context.cart.clear()        
        utils.flash(self.request, _(u"Der Bestellvorgang wurde abgebrochen."))
        self.request.response.redirect(self.portal_url+'/medien/medienkatalog/')

    @form.action(_(u'E-Mail-Bestellung'), validator=validate_checkout)
    def handle_order(self, action, data):
        plone = getToolByName(self.context, 'portal_url').getPortalObject()

        # We create the folder
        if not ORDERS in plone:
            plone[ORDERS] = OrderFolder(id=ORDERS)

        # We generate a unique id
        cid = str(uuid.uuid4())
        
        # we deepcopy the cart for more security.
        # It won't be altered later.
        cart = copy.deepcopy(self.context.cart)

        # We write down the shipping information
        shipping_information = ShippingInformation(id='shipping_information')
        utils.writeChanges(shipping_information, self.form_fields, data)

        # We instanciate an order.
        order = Order(cart, shipping_information, id=cid)

        # We write down the price. This won't be altered.
        order.total_price = self.context.handler.getTotalPrice()
        order.is_member = bool(self.context.is_member)

        # We write it down.
        plone[ORDERS][cid] = order
        self.context.cart.clear()        
        utils.flash(self.request,
                    _(u"Der Bestellvorgang ist bei uns eingegangen."))
        self.request.response.redirect(self.portal_url+'/medien/medienkatalog/++cart++/thanks?id=%s' % cid)

    @form.action(_(u'Fax-Bestellung'), validator=validate_checkout)
    def handle_print(self, action, data):
        plone = getToolByName(self.context, 'portal_url').getPortalObject()
        cid = str(uuid.uuid4())
        cart = copy.deepcopy(self.context.cart)
        shipping_information = ShippingInformation(id='shipping_information')
        utils.writeChanges(shipping_information, self.form_fields, data)
        order = Order(cart, shipping_information, id=cid)
        order.total_price = self.context.handler.getTotalPrice()
        order.is_member = bool(self.context.is_member)
        plone[TEMPORDERS][cid] = order
        self.context.cart.clear()        
        self.request.response.redirect(self.portal_url+'/medien/medienkatalog/++cart++/print?id=%s' % cid)

    def renderField(self, *args):
        label = required = description = error = input = "" 
        css_class = "field "
        for field in args:
            label += "%s " %field.label 
            if field.required:
                required = ('<span class="fieldRequired" title="Required"'
                            '>(Required)</span>')
            if field.hint:
                description += "%s " % field.hint
            if field.error():
                error += "%s " %field.error()
            input += "%s " %field().replace('id="form.', 'id="form_')    
            id = "field_" + field.name.replace('.', '_')
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


class Print(grok.View):
    grok.context(ISessionCart)
   

class Thanks(grok.View):
    grok.context(ISessionCart)


class pdf(grok.View):
    grok.context(ISessionCart)

    def render(self, id=None, temp=None):
        plone = getToolByName(self.context, 'portal_url').getPortalObject()
        if id:
            if temp:
                orders = plone[TEMPORDERS]
                order = orders.get(id)
            else:
                orders = plone[ORDERS]
                order = getattr(orders, id, None)
            if order:
                pdf = order.asPDF()
                RESPONSE = self.request.response
                RESPONSE.setHeader('content-type', 'application/pdf')
                RESPONSE.setHeader('content-length', str(len(pdf)))
                RESPONSE.setHeader('content-disposition', 'attachment; filename=Bestellung.pdf')
                return pdf
        return 

class ShippingInformationView(grok.DisplayForm):
    grok.name("index")
    grok.context(IOrderForm)
    grok.require("zope2.View")

    @property
    def label(self):
        return self.context.title
