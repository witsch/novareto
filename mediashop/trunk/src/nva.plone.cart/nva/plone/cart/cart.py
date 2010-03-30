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

from nva.mediashop.pdf.pdfgenMS import createpdf
from nva.mediashop.pdf.textgen  import createtext

class OrderFolder(Container):
    """A Cart folder implementation.
    """
    implements(IOrderFolder)
    meta_type = portal_type = 'OrderFolder'
    manage_options = PortalFolderBase.manage_options

    def __setitem__(self, name, obj):
        name = name.encode('ascii') # may raise if there's a bugus id
        self._setObject(name, obj, set_owner=0)


class SessionCart(Item):
    """A cart living in the session.
    """
    implements(ICartWrapper, ISessionCart)
    meta_type = portal_type = 'TempFolder'
    Title = getTitle = lambda self:u"Cart"

    def __init__(self, cart, id="++cart++"):
        Item.__init__(self, id=id)
        self.cart = cart
        self.id = id

    @apply
    def _member():
        def pget(self):
            return bool(self.cart.get('__member__'))
        def pset(self, value):
            self.cart['__member__'] = bool(value)
        return property(pget, pset)

    @property
    def is_member(self):
        return self._member

    @property
    def handler(self):
        return ICartHandler(self.cart)


def nN(v):
    if not v:
        return ''
    return v


class Order(Item):
    """A persisted cart.
    """
    implements(ICartWrapper, IOrder)
    meta_type = portal_type = 'Order'
    Title = getTitle = lambda self:u"Order %s" % self.id
    manage_options = PortalFolderBase.manage_options

    is_member = True 

    def __init__(self, cart, shipping_information, id=None):
        Item.__init__(self, id=id)
        self.cart = cart
        self.shipping_information = shipping_information
        self.id = id

    @property
    def reference(self):
        return self.id


    def getData(self):
        si = self.shipping_information
        artikel = []
        for item in self.cart.itervalues():
            bestellung = {}
            bestellung['Anzahl']  = item.quantity
            bestellung['Artikel'] = item.title
            bestellung['Preis']   = item.total_price
            artikel.append(bestellung)

        daten = {}
        daten['Bestellung']  = artikel
        daten['Mwst']        = 'zzgl. Versandkosten und gesetzl. MwSt.'
        daten['VornameName'] = si.vorname + ' ' + si.name
        daten['Mitglnr']     = nN(si.mitgliedsnummer)
        daten['Firma']       = si.firma
        daten['Strasse']     = si.strasse
        daten['PlzOrt']      = si.plz + ' ' + si.ort
        daten['Telefon']     = nN(si.telefon)
        daten['Telefax']     = nN(si.telefax)
        daten['Email']       = si.email
        daten['Land']        = nN(si.land)
        daten['Ustid']       = nN(si.ustid)
        daten['Abwadr']      = si.lieferadresse
        if si.lieferadresse:
            daten['ALFirma'] = si.lfirma  # Abweichende Lieferadresse
            daten['ALVornameName'] = si.lname  # Abweichende Lieferadresse
            daten['ALStrasse']     = si.lstrasse
            daten['ALPlzOrt']      = si.lplz + ' ' + si.lort

        return  daten


    def asPDF(self):

        daten = self.getData()

        #return createpdf('/Users/cklinger/Desktop/order.pdf', daten)
        file = "/tmp/order-%s.pdf" % self.id
        return createpdf(file, daten)


    def asText(self):

        daten = self.getData()

        return createtext(daten)


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
