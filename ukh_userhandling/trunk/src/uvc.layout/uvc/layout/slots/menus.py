# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok

from megrok.menu import Menu
from uvc.layout.interfaces import *


class GlobalMenu(Menu):
    grok.implements(IGlobalMenu)
    grok.name('globalmenu')


class Footer(Menu):
    grok.implements(IFooter)
    grok.name('footer')


class PersonalMenu(Menu):
    grok.implements(IPersonalMenu)
    grok.name('personalmenu')
