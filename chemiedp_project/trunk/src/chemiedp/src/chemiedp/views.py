import uvclight
from uvc.api import api

class Index(api.Page):
    api.context(uvclight.IRootObject)

    def render(self):
        import pdb;pdb.set_trace()
        return "Hallo Welt"

