# -*- coding: utf-8 -*-


import uvclight
from uvc.api import api
from uvc.design.canvas.menus import IAddMenu
from chemiedp.models import Hersteller, Reinigungsmittel
from chemiedp.interfaces import IHersteller, IReinigungsmittel


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


class AddReinigungsmittel(api.AddForm):
    api.context(IHersteller)
    fields = api.Fields(IReinigungsmittel)

    def create(self, data):
        rm = Reinigungsmittel(**data)
        return rm

    def add(self, obj):
        key = "Reinigungsmittel-%s" % len(self.context)
        self.context[key] = obj

    def nextURL(self):
        return self.url(self.context)


class AddMenuHersteller(uvclight.MenuItem):
    uvclight.menu(IAddMenu)
    api.context(uvclight.IRootObject)
    api.name('addhersteller')
    api.title('Hersteller adden')


class AddMenuReinigungsmittel(uvclight.MenuItem):
    uvclight.menu(IAddMenu)
    api.context(IHersteller)
    api.name('addreinigungsmittel')
    api.title('Reinigungsmittel adden')


class EditHersteller(api.EditForm):
    api.context(IHersteller)
    api.name('edit')
    fields = api.Fields(IHersteller)


class ViewHersteller(api.DisplayForm):
    api.context(IHersteller)
    api.name('index')
    fields = api.Fields(IHersteller)


class ViewReinigungsmittel(api.DisplayForm):
    api.context(IReinigungsmittel)
    api.name('index')
    fields = api.Fields(IReinigungsmittel)


class EditReinigungsmittel(api.EditForm):
    api.context(IReinigungsmittel)
    api.name('edit')
    fields = api.Fields(IReinigungsmittel)
