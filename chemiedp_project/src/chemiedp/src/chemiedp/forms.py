# -*- coding: utf-8 -*-
import uvclight
from uvc.api import api
from chemiedp.interfaces import IHersteller, IDruckbestaeubungspuder, IReinigungsmittel
from chemiedp.models import Hersteller, Druckbestaeubungspuder
from uvc.design.canvas.menus import IAddMenu, IGlobalMenu, IPersonalMenu, IFooterMenu, INavigationMenu

class AddHersteller(api.AddForm):
    api.context(uvclight.IRootObject)
    fields = api.Fields(IHersteller)
    label = u"Hersteller"
    description = u"Hier können Sie Hersteller anlegen."

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
    template = uvclight.get_template('herstellerviewtemplate.cpt', __file__)

class AddPuder(api.AddForm):
    api.context(IHersteller)
    fields = api.Fields(IDruckbestaeubungspuder)

    def create(self, data):
        puder = Druckbestaeubungspuder(**data)
        return puder

    def add(self, obj):
        self.context[obj.name] = obj

    def nextURL(self):
        return self.url(self.context)

class EditPuder(api.EditForm):
    api.context(IDruckbestaeubungspuder)
    api.name('edit')
    fields = api.Fields(IDruckbestaeubungspuder)

class ViewPuder(api.DisplayForm):
    api.context(IDruckbestaeubungspuder)
    api.name('index')
    fields = api.Fields(IDruckbestaeubungspuder)

