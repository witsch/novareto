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
         if self.context.absolute_url().startswith('http://'):
             src = src.replace('https://', 'http://')
         elif self.context.absolute_url().startswith('https://'):
             src = src.replace('http://', 'https://')
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
         showtitle = showdescription = False
         if hasattr(self.context, 'showtitle'):
             showtitle = self.context.showtitle
         if hasattr(self.context, 'showdescription'):
             showdescription = self.context.showdescription
         self.showtitle = showtitle
         self.showdescription = showdescription
