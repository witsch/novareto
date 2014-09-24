# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import uvclight
from uvc.api import api
from zope.interface import Interface


class Index(api.Page):
    api.context(Interface)
    template = uvclight.get_template('index.cpt', __file__)
