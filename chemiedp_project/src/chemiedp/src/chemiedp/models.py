# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from uvc.content import schema
from uvc.content import schematic_bootstrap
from uvclight.backends.zodb import Container, Content
from chemiedp.interfaces import IHersteller, IReinigungsmittel


class Hersteller(Container):
    schema(IHersteller)

    def __init__(self, **kwargs):
        super(Hersteller, self).__init__()
        schematic_bootstrap(self, **kwargs)


class Reinigungsmittel(Content):
    schema(IReinigungsmittel)

    def __init__(self, **kwargs):
        schematic_bootstrap(self, **kwargs)
