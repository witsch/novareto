import five.grok as grok
from nva.mediashop.content import IArtikel

grok.templatedir("templates")


class ArticleView(grok.View):
    """Displays a shop article.
    """
    grok.context(IArtikel)


    def getParentUrl(self):
        return self.url(self.context.aq_inner.aq_parent)
