from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from nva.moderatorenliste import moderatorenlisteMessageFactory as _

class IModeratorenliste(Interface):
    """Moderatorenliste"""
    
    # -*- schema definition goes here -*-
    name = schema.TextLine(
        title=_(u"New Field"), 
        required=False,
        description=_(u"Field description"),
    )

    mitgieldsnummer = schema.TextLine(
        title=_(u"Mitgliedsnummer"), 
        required=True,
        description=_(u"Bitte geben Sie hier die Mitgliedsnummer ein."),
    )

