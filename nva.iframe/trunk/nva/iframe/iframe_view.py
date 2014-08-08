# -*- coding: utf-8 -*-
from uvc.api import api
from zope.interface import Interface

api.templatedir('templates')

class iFrameView(api.Page):
     api.context(Interface)

     def update(self):
         callid = self.request.get('CallID', '') + ';' + self.request.get('DetailID', '')
         if not callid or callid == ';':
             callid = self.context.callid
         src = self.context.src
         parameter = self.context.parameter
         baseurl = self.context.absolute_url()
         filename = ''
         if self.context.cssfile:
             filename = self.context.cssfile.filename
             if callid:
                 self.srcurl = src + '?CallID=' + callid + '&customstylesrc=' + baseurl + '/@@download/cssfile/' + filename
             else:
                 self.srcurl = src + '?customstylesrc=' + baseurl + '/@@download/cssfile/' + filename
         else:
             if callid:
                 self.srcurl = src + '?CallID=' + callid
             else:
                 self.srcurl = src
