from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from nva.webcodeproxy import webcodeproxyMessageFactory as _



class IWebcodeproxy(Interface):
    """Objekt zur Speicherung von Webcodes, die an externe Systeme ausgeliefert wurden."""

    # -*- schema definition goes here -*-
    extsystems = schema.List(
        title=_(u"Ids externer Systeme"),
        required=True,
        description=_(u"Hier koennen die mit den externen Systemen vereinbarten IDs eingetragen werden. Die Ids muessen mitgeliefert werden, um einen Webcode zu erhalten."),
    )
#
    webcodes = schema.List(
        title=_(u"Webcodes"),
        required=False,
        description=_(u"Speicherung der Webcodes, die an externe Systeme ausgeliefert wurden."),
    )
#
