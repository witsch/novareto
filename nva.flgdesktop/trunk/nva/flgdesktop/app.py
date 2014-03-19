# -*- coding: utf-8 -*-
from five import grok
from uvc.api import api as uvcsite
from zope.interface import Interface

grok.templatedir('templates')

class FlgDesktop(uvcsite.Page):
    grok.context(Interface)
