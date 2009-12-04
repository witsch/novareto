# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute, moduleProvides

from nva.mediashop.content.medienshop import MedienShop
from nva.mediashop.content.kategorie import Kategorie
from nva.mediashop.content.artikel import Artikel
from nva.mediashop.content.shippinginfo import ShippingInformation
from nva.mediashop.interfaces import (
    IMedienShop, IKategorie, IArtikel, IOrderForm)


class IShopContents(Interface):
    """The Public Content API
    """
    MedienShop  = Attribute("The shop containing caterogies.")
    IMedienShop = Attribute("Represents a shop.")

    Kategorie  = Attribute("A shop category. Contains articles.")
    IKategorie = Attribute("Represents a shop category.")
    
    Artikel  = Attribute("A shop article.")
    IArtikel = Attribute("Represents a shop article item.")

    ShippingInformation = Attribute("Shipping information.")
    IOrderForm = Attribute("Represents the customer address information.")

moduleProvides(IShopContents)
__all__ = list(IShopContents)
