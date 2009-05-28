## Script (Python) "hasFacets"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=results
##title=
##
facets = None
if len(results) > 0:
    result = results[-1]
    facets = getattr(result, 'facet_count', None)
    context.plone_log(facets)
    #if facets:
#	return facets.get('facet_fields',{})
return facets
