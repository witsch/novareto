from zope.interface import Interface
from uvc.api import api


class Index(api.Page):
    api.context(Interface)

    def render(self):
        return "Das ist meine Startseite"
