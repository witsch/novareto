# -*- coding: utf-8 -*-
import uvclight
from uvc.api import api
from .interfaces import IHersteller
from zope.interface import Interface

class Index(api.Page):
    api.context(uvclight.IRootObject)
    template = uvclight.get_template('index.cpt', __file__)


class DisplayHersteller(api.Page):
    api.context(IHersteller)
    api.name('index')

    template = uvclight.get_template('hersteller.cpt', __file__)


class Hersteller(api.Page):
    api.context(uvclight.IRootObject)
    template = uvclight.get_template('herstellertemplate.cpt', __file__)

    def getFolderContents(self, items):
        objectlist = []
        for i in items:
            objdata = {}
            item = i[1]
            objdata['title'] = item.title
            objdata['url'] = self.url(item)
            objectlist.append(objdata)
        return objectlist

    def createRefsSnippet(self, objectlist):
        """Return a Html-Snippet with an unnumbered list"""
        if not objectlist:
            return ''
        snippet = '<ul>'
        for i in objectlist:
            row = '<li><a href="%s">%s</a></li>' %(i.get('url'),i.get('title'))
            snippet += row
        snippet += '</ul>'
        return snippet

    def update(self):
        objectlist = []
        for i in self.context.values():
            objdata = {}
            if i.__class__.__name__ == 'Hersteller':
                objdata['title'] = i.title
                objdata['url'] = self.url(i)
                objdata['email'] = i.email
                objdata['telefon'] = i.telefon
                objdata['homepage'] = i.homepage
                folderobjects = self.getFolderContents(i.items())
                objdata['objlist'] = self.createRefsSnippet(folderobjects)
                objectlist.append(objdata)
                self.objectdaten = objectlist

