from five import grok
from nva.mediashop.interfaces import IMedienShop, IKategorie

grok.templatedir('templates')

class Index(grok.Form):
    grok.context(IMedienShop)
    categories = []

    def update(self):
        request = self.request
        print request.text()
        self.categories = self.context.objectIds()


    @grok.action('Suchen')
    def handle_search(self, **kw):
        import pdb; pdb.set_trace() 
