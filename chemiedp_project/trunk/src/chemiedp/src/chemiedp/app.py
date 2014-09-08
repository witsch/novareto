# -*- coding: utf-8 -*-
from zope.interface import Interface
import uvclight
from uvclight.backends.zodb import Content, Container
from uvc.content import schema
from uvc.content import schematic_bootstrap
from uvc.api import api
from chemiedp.interfaces import IHersteller, IDruckbestaeubungspuder


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


class EditHersteller(api.EditForm):
    api.context(IHersteller)
    api.name('edit')
    fields = api.Fields(IHersteller)


class ViewHersteller(api.DisplayForm):
    api.context(IHersteller)
    api.name('index')
    fields = api.Fields(IHersteller)


class Hersteller(Container):
    schema(IHersteller)

    def __init__(self, **kwargs):
        super(Hersteller, self).__init__()
        schematic_bootstrap(self, **kwargs)
