from five import grok
from nva.mediashop.interfaces import IMedienShop, IKategorie
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

grok.templatedir('templates')

class Index(grok.Form):
    grok.context(IMedienShop)
    categories = []
    results = False

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def update(self):
        self.categories = self.context.objectIds()

    @grok.action('Suchen')
    def handle_search(self, **kw):
        artikel = self.request.get('form.artikel', None)
        if artikel:
            self.results = self.portal_catalog(portal_type="Artikel", searchableText=artikel)
            message = "Es wurden %s Ergebnisse gefunden" %len(self.results)
        else:
            message="Bitte geben Sie einen Suchbegriff ein" 
         
        IStatusMessage(self.request).addStatusMessage(message, type="info")
