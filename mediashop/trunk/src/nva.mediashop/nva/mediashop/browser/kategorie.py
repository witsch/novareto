from five import grok
from nva.mediashop.interfaces import IMedienShop, IKategorie
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

grok.templatedir('templates')

class Index(grok.Form):
    grok.context(IKategorie)
    grok.template('kategorie_view')
    results = []

    def update(self):
        self.results = self.context.getFolderContents(full_objects=True)

    @property
    def showDownload(self):
        show = False
        for artikel in self.results:
            if artikel.file.get_size() > 0:
                show = True
        return show

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @grok.action('Suchen')
    def handle_search(self, **kw):
        artikel = self.request.get('form.artikel', None)
        if artikel:
            if not artikel[-1] == '*':
                artikel += '*'
            path = '/'.join(self.context.getPhysicalPath())[1:]
            self.results = [x.getObject() for x in self.portal_catalog(
                  portal_type="Artikel", 
                  SearchableText=artikel, 
                  path=path)]
            message = "Es wurden %s Ergebnisse gefunden" %len(self.results)
        else:
            message="Bitte geben Sie einen Suchbegriff ein" 
         
        IStatusMessage(self.request).addStatusMessage(message, type="info")
