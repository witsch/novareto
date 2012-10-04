from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SeminarMetaViewlet(ViewletBase):

    index = ViewPageTemplateFile("seminarmeta.pt")

    def update(self):
        super(SeminarMetaViewlet, self).update()
        self.titel = self.request.form.get('titel')
        self.sort = self.request.form.get('sort')
        self.von = self.request.form.get('von')
        self.bis = self.request.form.get('bis')
        self.ausgebucht = self.request.form.get('ausgebucht')
        self.folge1 = self.request.form.get('folge1')
        self.folge2 = self.request.form.get('folge2')
