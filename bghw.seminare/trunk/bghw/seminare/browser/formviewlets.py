from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SeminarMetaViewlet(ViewletBase):

    index = ViewPageTemplateFile("seminarmeta.pt")

    def update(self):
        super(SeminarMetaViewlet, self).update()
        self.sort = self.context.sort
        self.von = self.context.von
        self.bis = self.context.bis
