# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains, containers

from nva.mediashop import mediashopMessageFactory as _


class IArtikel(Interface):
    """Artikel"""
    
    # -*- schema definition goes here -*-
    status = schema.TextLine(
        title=_(u"Article status"), 
        required=False,
        description=_(u"Availability of the article"),
    )

    preis = schema.Float(
        title=_(u"Preis"), 
        required=False,
        description=_(u"Price"),
    )

    preisinfo = schema.TextLine(
        title=_(u"Preisinfo"), 
        required=False,
        description=_(u"Priceinfo"),
    )

    text = schema.Text(
        title=_(u"Text"), 
        required=False,
        description=_(u"Article description"),
    )

    tax = schema.Text(
        title=_(u"Tax"), 
        required=False,
        description=_(u"Tax information"),
    )

    code = schema.TextLine(
        title=_(u"Artikel Nummer"), 
        required=False,
    )

    quantity = schema.TextLine(
        title=_(u"Quantity"), 
        required=False,
    )

    image = schema.Bytes(
        title=_(u"Image"), 
        required=False,
    )

    file = schema.Bytes(
        title=_(u"File"), 
        required=False,
    )
