# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok
from uvc.layout.interfaces import *
from zope.interface import Interface
from dolmen.app.layout import master


class Headers(master.Header):
    """Viewlet Manager for the Header
    """
    grok.name('uvc-headers')
    grok.context(Interface)
    grok.implements(IHeaders)


class AboveContent(master.AboveBody):
    grok.name('uvc-above-body')
    grok.context(Interface)
    grok.implements(IAboveContent)


class BelowContent(master.BelowBody):
    grok.name('uvc-below-body')
    grok.context(Interface)
    grok.implements(IBelowContent)


class PageTop(master.Top):
    """ViewletManager for the PageTop
    """
    grok.name('uvc-pagetop')
    grok.context(Interface)
    grok.implements(IPageTop)
    grok.require('zope.View')


class Footer(master.Footer):
    """ViewletManager for the PageTop
    """
    grok.name('uvc-footer')
    grok.context(Interface)
    grok.implements(IFooter)
    grok.require('zope.View')

