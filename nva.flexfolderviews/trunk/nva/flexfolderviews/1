# -*- coding:utf-8 -*-
from uvc.api import api 
from zope.interface import Interface

api.templatedir('templates')

def createFullContent(obj):
    myobj = {}
    myobj['id'] = obj.id
    myobj['title'] = obj.title
    myobj['description'] = obj.Description().decode('utf-8')
    myobj['text'] = ''
    myobj['details'] = ''
    if obj.portal_type == 'Document':
        myobj['text'] = obj.getText().decode('utf-8')
    elif obj.portal_type == 'bgetem.praevention.dokupraevention':
        myobj['text'] = obj.haupttext.decode('utf-8')
        myobj['details'] = obj.details.decode('utf-8')
    return myobj

class CarouselView(api.Page):
    api.context(Interface)

    def update(self):
        contents = self.context.getFolderContents()
        foldercontents = []
        acco_id = 0
        for i in contents:
             obj = i.getObject()
             myobj = createFullContent(obj)
             myobj['subobjects'] = []
             if obj.portal_type == 'Folder':
                 subcontents = obj.getFolderContents()
                 carou_id = 0
                 for j in subcontents:
                     subobj = createFullContent(j.getObject())
                     subobj['carou_id'] = carou_id
                     subobj['class'] = 'item'
                     subobj['liclass'] = ''
                     if carou_id == 0:
                         subobj['class'] = 'item active'
                         subobj['liclass'] = 'active'
                     myobj['subobjects'].append(subobj)
                     carou_id += 1
             myobj['acco_id'] = acco_id
             acco_id += 1
             foldercontents.append(myobj)
        self.foldercontents = foldercontents

class TabView(api.Page):
    api.context(Interface)

    def update(self):
        contents = self.context.getFolderContents()
        foldercontents = []
        tabcontents = []
        main_id = 0
        for i in contents:
            obj = i.getObject()
            myobj = createFullContent(obj)
            myobj['subobjects'] = []
            myobj['class'] = ''
            myobj['datatoggle'] = 'tab'
            myobj['tabclass'] = 'tab-pane fade'
            if main_id == 0:
                myobj['class'] = 'active'
                myobj['tabclass'] = 'tab-pane fade in active'
            if obj.portal_type == 'Folder':
                myobj['class'] = 'dropdown ' + myobj['class']
                myobj['datatoggle'] = 'dropdown'
                subcontents = obj.getFolderContents()
                sub_id = 0
                for j in subcontents:
                    subobj = createFullContent(j.getObject())
                    subobj['tabclass'] = 'tab-pane fade'
                    if main_id == 0 and sub_id == 0:
                        subobj['tabclass'] = 'tab-pane fade in active'
                    tabcontents.append(subobj)
                    myobj['subobjects'].append(subobj)
                    sub_id += 1
            else:
                tabcontents.append(myobj)
            main_id += 1
            foldercontents.append(myobj)
        self.foldercontents = foldercontents
        self.tabcontents = tabcontents
