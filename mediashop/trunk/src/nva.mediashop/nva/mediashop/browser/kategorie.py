from five import grok
from nva.mediashop.interfaces import IMedienShop, IKategorie
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

grok.templatedir('templates')

class Index(grok.View):
    grok.context(IKategorie)
    grok.template('kategorie_view')
    artikel = []

    def update(self):
        self.artikel = self.context.getFolderContents(full_objects=True)

    @property
    def showDownload(self):
        show = False
        for artikel in self.artikel:
            if artikel.file.get_size() > 0:
                show = True
        return show
