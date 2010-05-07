from five import grok
from nva.mediashop.interfaces import IMedienShop, IKategorie
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

grok.templatedir('templates')

class Index(grok.Form):
    grok.context(IMedienShop)
    grok.template('mediashop_view')
    categories = []
    results = False

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def update(self):
        self.categories = [dict(title=x.Title, url=x.getURL()) for x in self.context.getFolderContents()] 
        #self.categories.append(dict(title='Alle Artikel', url=self.url(self.context, 'all')))

    @grok.action('Suchen')
    def handle_search(self, **kw):
        artikel = self.request.get('form.artikel', None)
        if artikel:
            if not artikel[-1] == '*':
                artikel += '*'
            self.results = self.portal_catalog(portal_type="Artikel", SearchableText=artikel)
            message = "Es wurden %s Ergebnisse gefunden" %len(self.results)
        else:
            message="Bitte geben Sie einen Suchbegriff ein" 
         
        IStatusMessage(self.request).addStatusMessage(message, type="info")

    @property
    def showDownload(self):
        show = False
        for artikel in self.results:
            artikel = artikel.getObject()
            if artikel.file.get_size() > 0:
                show = True
        return show

        

class All(grok.View):
    grok.context(IMedienShop)
    results = []

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def update(self):
        tmp_results = []
        for rubrik in self.context.values():
            for artikel in rubrik.values():
                if not artikel.index_html == None:
                    tmp_results.append(artikel) 
        self.results = tmp_results 

    @grok.action('Suchen')
    def handle_search(self, **kw):
        r = False
        artikel = self.request.get('form.artikel', None)
        if artikel:
            if not artikel[-1] == '*':
                artikel += '*'

            self.results = [x.getObject() for x in self.portal_catalog(portal_type="Artikel", SearchableText=artikel)]
            message = "Es wurden %s Ergebnisse gefunden" %len(self.results)
            r = True
        else:
            message="Bitte geben Sie einen Suchbegriff ein" 
         
        IStatusMessage(self.request).addStatusMessage(message, type="info")
        if r:
            self.redirect(self.url(self.context))

    @property
    def showDownload(self):
        show = False
        for artikel in self.results:
            artikel = artikel.getObject()
            if artikel.file.get_size() > 0:
                show = True
        return show

