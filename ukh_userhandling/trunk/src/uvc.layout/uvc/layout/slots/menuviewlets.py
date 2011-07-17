# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
from zope.interface import Interface
from zope.component import getUtility
from zope.browsermenu.interfaces import IBrowserMenu
from uvc.layout.interfaces import IPageTop, IFooter


grok.templatedir('templates')


class GlobalMenuViewlet(grok.Viewlet):
    grok.viewletmanager(IPageTop)
    grok.context(Interface)
    grok.order(20)

    id = "globalmenuviewlet"

    def update(self):
        self.menus = getUtility(IBrowserMenu, 'globalmenu').getMenuItems(self.context, self.request)
        return self.menus


class PersonalMenuViewlet(grok.Viewlet):
    grok.viewletmanager(IPageTop)
    grok.context(Interface)
    grok.order(40)

    id = "personalmenuviewlet"

    def update(self):
       self.menus = getUtility(IBrowserMenu, 'personalmenu').getMenuItems(self.context, self.request)
       return self.menus


class FooterViewlet(grok.Viewlet):
    grok.viewletmanager(IFooter)
    grok.context(Interface)
    grok.order(10)

    id = "footerviewlet"

    def update(self):
       self.menus = getUtility(IBrowserMenu, 'footer').getMenuItems(self.context, self.request)
       return self.menus
