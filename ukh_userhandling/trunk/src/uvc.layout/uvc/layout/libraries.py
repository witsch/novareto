# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grokcore.viewlet as grok

from fanstatic import Library, Resource
from js.jquery import jquery
from megrok import resourceviewlet
from zope.interface import Interface


library = Library('example', 'static')

ie = Resource(library, 'ie.css')
pr = Resource(library, 'print.css')
screen = Resource(library, 'screen.css')
fancy = Resource(library, 'fancy.css')
superfish = Resource(library, 'superfish.js')
superfish_css = Resource(library, 'superfish.css')
main_css = Resource(library, 'main.css')

class LightBlueResourceViewlet(resourceviewlet.ResourceViewlet):
    grok.context(Interface)
    resources = [ie, screen, fancy, jquery, superfish, superfish_css, main_css]

