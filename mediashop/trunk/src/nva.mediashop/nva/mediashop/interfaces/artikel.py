from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from nva.mediashop import mediashopMessageFactory as _

class IArtikel(Interface):
    """Artikel"""
    
    # -*- schema definition goes here -*-
    status = schema.TextLine(
        title=_(u"New Field"), 
        required=False,
        description=_(u"Field description"),
    )

    preis = schema.Float(
        title=_(u"Preis"), 
        required=False,
        description=_(u"Field description"),
    )

    stand = schema.TextLine(
        title=_(u"New Field"), 
        required=False,
        description=_(u"Field description"),
    )

    text = schema.Text(
        title=_(u"Text"), 
        required=False,
        description=_(u"Field description"),
    )

    artikel_nr = schema.TextLine(
        title=_(u"Artikel Nummer"), 
        required=False,
        description=_(u"Field description"),
    )

