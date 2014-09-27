# -*- coding: utf-8 -*-

from uvclight.backends.zodb import Root, ZODBPublication
from uvclight import IRootObject
from zope.interface import implements
#from uvc.bootstraptheme import IBootstrapThemeRequest
from uvc.themes.dguv import IDGUVRequest


class MyRoot(Root):
    implements(IRootObject)
    title = u"Datenbank Druckbestäubungspuder"


class Application(ZODBPublication):
    layers = [IDGUVRequest, ]
    root = MyRoot
