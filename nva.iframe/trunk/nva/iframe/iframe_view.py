# -*- coding: utf-8 -*-
from uvc.api import api
from zope.interface import Interface

api.templatedir('templates')

class iFrameView(api.Page):
     api.context(Interface)

