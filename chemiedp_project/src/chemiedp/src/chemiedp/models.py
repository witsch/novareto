from uvc.api import api
from chemiedp.interfaces import IHersteller, IDruckbestaeubungspuder
from uvc.content import schema
from uvc.content import schematic_bootstrap
from uvclight.backends.zodb import Container, Content
from chemiedp.interfaces import IHersteller, IReinigungsmittel


class Hersteller(Container):
    schema(IHersteller)

    def __init__(self, **kwargs):
        super(Hersteller, self).__init__()
        schematic_bootstrap(self, **kwargs)

class Druckbestaeubungspuder(Content):
    schema(IDruckbestaeubungspuder)

    def __init__(self, **kwargs):
        super(Druckbestaeubungspuder, self).__init__()
        schematic_bootstrap(self, **kwargs)
