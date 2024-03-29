# -*- coding:utf-8 -*-
from uvc.api import api
from zope.interface import Interface

api.templatedir('templates')

class FluidView(api.Page):
    api.context(Interface)

    def createFullContent(self, obj, objcount=None):
        myobj = {}
        myobj['id'] = obj.id
        myobj['title'] = obj.title
        myobj['description'] = obj.Description().decode('utf-8')
        myobj['text'] = ''
        myobj['details'] = ''
        myobj['count'] = objcount
        if obj.portal_type == 'Document':
            myobj['text'] = obj.getText().decode('utf-8')
        elif obj.portal_type == 'bgetem.praevention.dokupraevention':
            myobj['text'] = obj.haupttext.output
            if obj.details:
                myobj['details'] = obj.details.output
        return myobj

    def update(self):
        contents = self.context.getFolderContents()
        fullcontents = []
        folders = []
        foldercount = 0
        for i in contents:
            obj = i.getObject()
            if obj.portal_type == 'Folder':
                folderobj = {}
                folderobj['objects'] = []
                folderobj['count'] = foldercount
                folderobj['title'] = obj.title
                folderobj['description'] = obj.Description().decode('utf-8')
                foldercontents = obj.getFolderContents()
                objcount = 0
                for j in foldercontents:
                    subobj = j.getObject()
                    folderobj['objects'].append(self.createFullContent(subobj, objcount))
                    objcount += 1
                folders.append(folderobj)
                foldercount += 1
            else:
                myobj = self.createFullContent(obj)
                fullcontents.append(myobj)
        N = 3 #Anzahl der Spalten im FluidView
        self.subList = [fullcontents[n:n+N] for n in range(0, len(fullcontents), N)]
        self.fullList = []
        if len(fullcontents) < 3:
            self.subList = []
            self.fullList = fullcontents
        self.Folders = folders
        self.Documentorder = True
        if hasattr(self.context, 'documentorder'):
            self.Documentorder = self.context.documentorder
