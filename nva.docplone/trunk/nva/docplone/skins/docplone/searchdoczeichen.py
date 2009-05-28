## Script (Python) "searchdoczeichen"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
docz = getattr(context,'doczeichen',None)
if docz:
        return ''.join(docz)

