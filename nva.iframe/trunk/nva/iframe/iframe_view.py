# -*- coding: utf-8 -*-
from uvc.api import api
from zope.interface import Interface

api.templatedir('templates')

class iFrameView(api.Page):
     api.context(Interface)

     def update(self):
         src = self.context.src
         parameter = self.context.parameter
         baseurl = self.context.absolute_url()
         filename = ''
         if self.context.cssfile:
             filename = self.context.cssfile.filename
         self.srcurl = src + parameter + 'customstylesrc=' + baseurl + '/@@download/cssfile/' + filename
