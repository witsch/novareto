# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from zope.interface import Interface
from uvc.api import api
from nva.chemiedp.herstellerordner import IHerstellerOrdner

api.templatedir('viewtemplates')


def back_references(source_object, attribute_name):
    """ Return back references from source object on specified attribute_name """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                            dict(to_id=intids.getId(aq_inner(source_object)),
                                 from_attribute=attribute_name)
                            ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result

def createRefsSnippet(objectlist):
    """Return a Html-Snippet with an unnumbered list"""
    snippet = '<ul>'
    for i in objectlist:
        row = '<li><a href="%s">%s</a></li>' %(i.absolute_url(),i.title)
        snippet += row
    snippet += '</ul>'
    return snippet

class HerstellerOrdnerView(api.Page):
    api.context(IHerstellerOrdner)
    
    def update(self):
        fc = self.context.getFolderContents()
        objlist=[]
        for i in fc:
            entry={}
            obj=i.getObject()
            entry["backrefs"] = createRefsSnippet(back_references(obj, 'hersteller'))
            entry["title"]=obj.title
            entry["url"]=obj.absolute_url()
            entry["homepage"]=obj.homepage
            entry["email"]=obj.email
            objlist.append(entry)
        self.objlist= objlist

