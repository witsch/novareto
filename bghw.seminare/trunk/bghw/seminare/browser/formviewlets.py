from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SeminarMetaViewlet(ViewletBase):

    index = ViewPageTemplateFile("seminarmeta.pt")

    def update(self):
        super(SeminarMetaViewlet, self).update()
        try:
            self.titel = self.request.get('titel', self.context.titel.get(self.context))
            self.sort = self.request.get('sort', self.context.sort.get(self.context))
            self.von = self.request.get('von', self.context.von.get(self.context))
            self.bis = self.request.get('bis', self.context.bis.get(self.context))
        except:
            self.titel = ''
            self.sort = ''
            self.von = ''
            self.bis = ''
