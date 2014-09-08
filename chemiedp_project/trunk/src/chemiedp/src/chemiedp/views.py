import uvclight
from uvc.api import api

class Index(api.Page):
    api.context(uvclight.IRootObject)

    def render(self):
        return "Hallo Welt"

