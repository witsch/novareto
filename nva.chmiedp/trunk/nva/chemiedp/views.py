# -*- coding:utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from nva.chemiedp.herstellerordner import IHerstellerOrdner

api.templatedir('viewtemplates')

class HerstellerOrdnerView(api.Page):
    api.context(IHerstellerOrdner)
    
    def update(self):
        fc = self.context.getFolderContents()
        objlist=[]
        for i in fc:
            entry={}
            obj=i.getObject()
            entry["title"]=obj.title
            entry["url"]=obj.absolute_url()
            entry["homepage"]=obj.homepage
            entry["email"]=obj.email
            objlist.append(entry)
        self.objlist= objlist

