# -*- coding: utf-8 -*-

from uvclight.backends.zodb import Root, ZODBPublication
from uvclight import IRootObject
from zope.interface import implements
from uvc.bootstraptheme import IBootstrapThemeRequest


class MyRoot(Root):
    implements(IRootObject)
    title = "Wasch- und Reinigungsmitteldatenbank"


class Application(ZODBPublication):
    layers = [IBootstrapThemeRequest, ]
    root = MyRoot
