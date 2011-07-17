# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok

from zope.interface import Interface
from uvc.layout.interfaces import IPageTop


grok.templatedir('templates')


class BGHeader(grok.Viewlet):
    grok.viewletmanager(IPageTop)
    grok.context(Interface)
    grok.order(10)
