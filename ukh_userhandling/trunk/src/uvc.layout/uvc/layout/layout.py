# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de 

import grok
from dolmen.app.layout import master, skin
from zope.interface import Interface

grok.templatedir('templates')


class IUVCBaseLayer(skin.IBaseLayer):
    """
    """

class IUVCLayer(IUVCBaseLayer):
    """Base skin layer for an UVC Site
    """
    grok.skin('uvcskin')


class Layout(master.Master):
    grok.layer(IUVCBaseLayer)
    grok.name('uvc.layout')

    def update(self):
        master.Master.update(self)
