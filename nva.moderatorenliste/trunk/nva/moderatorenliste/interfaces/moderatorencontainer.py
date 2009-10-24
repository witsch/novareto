from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from nva.moderatorenliste import moderatorenlisteMessageFactory as _

class IModeratorenContainer(Interface):
    """A Container for Moderator Items"""
    
    # -*- schema definition goes here -*-
