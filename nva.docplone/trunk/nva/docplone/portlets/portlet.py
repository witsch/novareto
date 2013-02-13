from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.portlets.portlets import base
from plone.memoize import request
from plone.memoize.interfaces import ICacheChooser
	
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider

from nva.docplone import MessageFactory as _

class IDocZeichenPortlet(IPortletDataProvider):
    """A portlet which shows Doczeichen."""

class Assignment(base.Assignment):
    """Portlet assignment.
    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IDocZeichenPortlet)

    def __init__(self, title="Doczeichen",zurueck=None,vor=None):
        self.__title__=title
        self.__link__=title
        self.__zurueck__=zurueck
        self.__vor__=vor

    @property
    def title(self):
        return self.__title__
    def link(self):
        return self.__link__
    def zurueck(self):
        return self.__zurueck__
    def vor(self):
        return self.__vor__

class Renderer(base.Renderer):
    """Portlet renderer.
    """
    render = ViewPageTemplateFile("portlet.pt")

    @property
    def title(self):
        return self.data.title
    def link(self):
        return self.data.link
    def zurueck(self):
        return self.data.zurueck
    def vor(self):
        return self.data.vor

    def showDoczeichen(self):
	""" Return the Doczeichen of the object """
	context = self.context
	rc=[]
	if not hasattr(context,'doczeichen'):
	    return rc
	try:
	    for doczeichen in context.doczeichen:

  	        pcat = context.portal_catalog
	        erg = pcat(doczeichen=doczeichen, 
                           sort_on='modified',
                           sort_order='revers', 
                           portal_type=['PloneArticle', 'Document', 'News Item'])
	        objlist=[]
                
                vor = ''
		zurueck = ''
		ind = 0
		
	        if len(erg) > 1:
	           for i in erg:
	              obj=i.getObject()
	              objlist.append(obj) 
		   try:
                       ind = objlist.index(context)
                   except:
		       ind = 0
	           try:
		       if ind > 0:
  	                  zurueck = objlist[ind-1].absolute_url
		       else:
		          zurueck = ''
	           except:
		       zurueck = ''
    	           try:
	                  vor = objlist[ind+1].absolute_url
	           except:
		       vor = ''
		link = doczeichen
		title = doczeichen + ' ('+str(ind+1) + '/' + str(len(erg) ) + ') '
	        d = {'title': title, 'link': link, 'zurueck': zurueck, 'vor': vor}
	        rc.append(d)
	except:
	    print "EXECPT"
	    return rc
	return rc 
 
class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(IDocZeichenPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IDocZeichenPortlet)
