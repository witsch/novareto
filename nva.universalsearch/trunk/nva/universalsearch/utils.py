facet = {'facet_fields': {'system': {'Intranet': 1, 'Extranet': 1, 'intranet': 0}}, 'facet_dates': {}, 'facet_queries': {}}
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
import Globals


class FacetResult(object):
    """ A Helper Class for Facett Results """

    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    facet = {}

    def __init__(self, facet):
	self.facet = facet

    def facets(self):
	""" This is a ds"""
	return self.facet.get('facet_fields').keys()

    security.declarePublic('getLinkGroup')
    def getLinkGroup(self, facet, url="", SearchableText=""):
	""" This is a ds"""
	res = []
	groups = self.facet.get('facet_fields').get(facet).items()
	for group, number in groups:
	    href = "%s/search?%s=%s&SearchableText=%s" %(url, facet, group, SearchableText)
	    link = '<a href="%s"> %s (%s) </a>' %(href, group, number)
	    res.append(link)
	return res 

Globals.InitializeClass(FacetResult)

if __name__ == '__main__':
    fr = FacetResult(facet)
    print fr.facets()
