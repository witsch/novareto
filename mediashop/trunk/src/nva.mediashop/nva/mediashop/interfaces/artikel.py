from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from nva.mediashop import mediashopMessageFactory as _

class IArtikel(Interface):
    """Artikel"""
    
    # -*- schema definition goes here -*-
