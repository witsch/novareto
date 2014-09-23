# -*- coding: utf-8 -*-
from zope.interface import Interface
import uvclight
from uvclight.backends.zodb import Content, Container
from uvc.content import schema
from uvc.content import schematic_bootstrap
from uvc.api import api
from chemiedp.interfaces import IHersteller
from chemiedp.models import Hersteller
from uvc.design.canvas.menus import IAddMenu, IGlobalMenu, IPersonalMenu, IFooterMenu


class AddHersteller(api.AddForm):
    api.context(uvclight.IRootObject)
    fields = api.Fields(IHersteller)

    def create(self, data):
        hersteller = Hersteller(**data)
        return hersteller

    def add(self, obj):
        self.context[obj.name] = obj

    def nextURL(self):
        return self.url(self.context)


class AddMenuItem(uvclight.MenuItem):
    uvclight.menu(IGlobalMenu)
    api.name('addhersteller')
    api.title('Hersteller adden')


class EditHersteller(api.EditForm):
    api.context(IHersteller)
    api.name('edit')
    fields = api.Fields(IHersteller)


class ViewHersteller(api.DisplayForm):
    api.context(IHersteller)
    api.name('index')
    fields = api.Fields(IHersteller)

