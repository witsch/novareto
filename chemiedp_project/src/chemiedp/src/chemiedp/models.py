from uvc.api import api
from chemiedp.interfaces import IHersteller
from uvc.content import schema
from uvc.content import schematic_bootstrap
from uvclight.backends.zodb import Container, Content

class Hersteller(Container):
    schema(IHersteller)

    def __init__(self, **kwargs):
        super(Hersteller, self).__init__()
        schematic_bootstrap(self, **kwargs)


