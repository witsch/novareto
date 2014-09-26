# -*- coding: utf-8 -*-
import uvclight
from uvc.api import api
from uvc.design.canvas.menus import IGlobalMenu, INavigationMenu
from chemiedp.interfaces import IHersteller

class HerstellerMenu(uvclight.MenuItem):
    uvclight.menu(INavigationMenu)
    api.name('hersteller')
    api.title('Hersteller')
    api.order(1)

class StartseiteMenu(uvclight.MenuItem):
    uvclight.menu(INavigationMenu)
    api.name('index')
    api.title('Startseite')
    api.order(0)

class AddHerstellerMenuItem(uvclight.MenuItem):
    uvclight.menu(IGlobalMenu)
    api.context(uvclight.IRootObject)
    api.name('addhersteller')
    api.title(u'Hersteller hinzufügen')

class AddPuderMenuItem(uvclight.MenuItem):
    uvclight.menu(IGlobalMenu)
    api.context(IHersteller)
    api.name('addpuder')
    api.title(u'Produkt hinzufügen')
