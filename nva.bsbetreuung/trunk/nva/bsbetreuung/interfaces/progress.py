from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from nva.onlinehandlungshilfe import onlinehandlungshilfeMessageFactory as _

class IProgress(Interface):
    """Marker-Interface fuer das Viewlet mit der Fortschrittsanzeige"""

