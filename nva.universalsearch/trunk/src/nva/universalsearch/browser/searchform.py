from five import grok
from zope.interface import Interface
from zope.schema import TextLine


from Products.CMFPlone.interfaces import IPloneSiteRoot
class ISearchMarker(Interface):
    SearchableText = TextLine(title=u"Suche", description=u"Bitte geben Sie hier Ihre Suche ein")
    system = TextLine(title=u"System", description=u"In welchem System wollen Sie suchen")

class UniversalSearch(grok.Form):
    grok.context(IPloneSiteRoot)
    grok.name('universalsearch')
    template = grok.PageTemplateFile('searchform.pt')
    form_fields = grok.Fields(ISearchMarker)

    @grok.action(u'Suche')
    def handle_search(self, **kw):
	print kw


    def __call__(self):
	self.request.set('disable_border', True)
	return super(UniversalSearch, self).__call__()

