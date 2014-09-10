# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import uvclight
from uvc.api import api
from uvclight import MenuItem
from uvc.design.canvas import IGlobalMenu, IPersonalMenu


class Index(api.Page):
    api.context(uvclight.IRootObject)

    def render(self):
        return "Hallo Welt"


class Startseite(MenuItem):
    api.name('index')
    api.title('Startseite')
    api.menu(IGlobalMenu)
    api.context(uvclight.IRootObject)


class Benutzername(MenuItem):
    api.name('benutzername')
    api.title('Benutzername')
    api.menu(IPersonalMenu)
    api.context(uvclight.IRootObject)
