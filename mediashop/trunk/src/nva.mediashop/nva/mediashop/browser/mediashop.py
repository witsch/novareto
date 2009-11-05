from five import grok
from nva.mediashop.interfaces import IMedienShop, IKategorie

grok.templatedir('templates')

class LandingPage(grok.View):
    grok.context(IMedienShop)
    categories = []

    def update(self):
        self.categories = self.context.objectItems()
