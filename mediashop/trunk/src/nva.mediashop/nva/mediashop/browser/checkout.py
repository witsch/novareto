# -*- coding: utf-8 -*-

import Acquisition
from zope import component
from zope.formlib import form
from AccessControl import getSecurityManager

from Products.CMFCore.utils import getToolByName
from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.PloneGetPaid.i18n import _
from Products.PloneGetPaid.browser.checkout import BaseCheckoutForm
from Products.PloneGetPaid.interfaces import (IGetPaidManagementOptions,
                                              IAddressBookUtility)
from Products.PloneGetPaid.browser.widgets import (CountrySelectionWidget,
                                                   StateSelectionWidget)

def null_condition( *args ):
    return ()

class CheckoutAddress(BaseCheckoutForm):

    sections = ('billing_address','shipping_address','contact_information')

    def customise_widgets(self,fields):
        fields['ship_country'].custom_widget = CountrySelectionWidget
        fields['bill_country'].custom_widget = CountrySelectionWidget
        fields['ship_state'].custom_widget = StateSelectionWidget
        fields['bill_state'].custom_widget = StateSelectionWidget

    template = ZopeTwoPageTemplateFile("templates/checkout-address.pt")

    def update( self ):
        formbase.processInputs( self.request )
        self.adapters = self.wizard.data_manager.adapters
        super(CheckoutAddress, self).update()

        # If the user has set up alternate opt-in language, use it instead
        opt_in_text = None
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        try:
            opt_in_text = IGetPaidManagementOptions(portal).alternate_opt_in_text
        except AttributeError:
            opt_in_text = None

        if opt_in_text and len(opt_in_text):
            formSchemas = component.getUtility(interfaces.IFormSchemas)
            widgets = self._getWidgetsByInterface(formSchemas.getInterface('contact_information'))

            for w in widgets:
                if w.name == 'form.marketing_preference':
                    w.context.title = opt_in_text

    def hasAddressBookEntries(self):
        """
        Do we have any entry?
        """
        book = component.getUtility(IAddressBookUtility).get(getSecurityManager().getUser().getId())
        return len(book.keys())

    def save_address(self, data):
        """
        store the address in the addressbook of the user
        """
        book_key = 'addressbook_entry_name'
        entry = self.wizard.data_manager.get( book_key )
        del self.wizard.data_manager[ book_key ]
        # if the user fill the name of the entry mean that we have to save the address
        if not entry:
            return
        elif isinstance( entry, list):
            entry = filter( None, entry)
            if not entry:
                return
            entry = entry[-1]

        uid = getSecurityManager().getUser().getId()
        if uid == 'Anonymous':
            return

        book  = component.getUtility(IAddressBookUtility).get( uid )
        if entry in book:
            return

        # here we get the shipping address
        formSchemas = component.getUtility(interfaces.IFormSchemas)
        ship_address_info = formSchemas.getBagClass('shipping_address')()
        if data['ship_same_billing']:
            for field in data.keys():
                if field.startswith('bill_'):
                    ship_address_info.__setattr__(
                        field.replace('bill_','ship_'), data[field])
        else:
            for field in data.keys():
                if field.startswith('ship_'):
                    ship_address_info.__setattr__(field, data[field])
        book[entry] = ship_address_info
        self.context.plone_utils.addPortalMessage(
            _(u'A new address has been saved'))

    @form.action(_(u"Continue"), name="continue")
    def handle_continue( self, action, data ):
        self.save_address(data)
        self.next_step_name = wizard_interfaces.WIZARD_NEXT_STEP

    @form.action(_(u"Cancel"), name="cancel", validator=null_condition)
    def handle_cancel( self, action, data):
        url = self.context.portal_url.getPortalObject().absolute_url()
        url = url.replace("https://", "http://")
        return self.request.response.redirect(url)
