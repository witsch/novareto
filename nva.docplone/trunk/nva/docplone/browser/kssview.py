from kss.core import kssaction
from kss.core import force_unicode
from zope.component import getUtility, getMultiAdapter
from Products.CMFCore.utils import UniqueObject, getToolByName
from plone.app.kss.plonekssview import PloneKSSView
from nva.docplone.interfaces import IDocZeichenUtility
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from plone.portlets.utils import hashPortletInfo, unhashPortletInfo	

info = dict(
     manager = 'plone.rightcolumn',
     category = 'context',
     key = '/arbeitshandbuch',   # Name of the Portal
     name = u'doczeichen',
     )

class KSSDocZeichen(PloneKSSView):
    """ KSSDocZeichen """

    @kssaction
    def addDocZeichen(self, form={}, portlethash=None):
	""" addDocZeichen 
            Achtung muss mich noch um multiple Doczeichen kuemmern
        """
        context = self.context
	request = self.request
        field = context.getField('doczeichen')
	doczeichen = request.get('ddzz','')
        error = self._validateDoczeichen(doczeichen)
        if error != None:
             self.getCommandSet('atvalidation').issueFieldError('doczeichen', error)
	     return
#	print "doczeichenreq", doczeichen
	value = list(field.get(context))
	value.append(doczeichen)
        field.set(context, value)
        context.reindexObject()
        system = getMultiAdapter((context, request), name="plone_portal_state")
        info['key'] = '/' + system.portal().getId() 
	portlethash = hashPortletInfo(info)
        self.getCommandSet('plone').refreshPortlet(portlethash)
	mac = self.macroField(field='doczeichen')
        core = self.getCommandSet('core')
	core.replaceHTML(core.getHtmlIdSelector('archetypes-fieldname-doczeichen'), mac)

    def _validateDoczeichen(self, doczeichen):
	error = None
	if len(doczeichen) <= 2:
	    error = "Das Doczeichen ist zu kurz"
	return error

    @kssaction
    def deleteDoczeichen(self, doczeichen=None, portlethash=None):
	""" Delete The Doczeichen """
        context = self.context
        field = context.getField('doczeichen')
	value = list(field.get(context))
#	print value
#	print "doczeichen", doczeichen
	value.remove(doczeichen)
	field.set(context, value)
	context.reindexObject()
	portlethash = hashPortletInfo(info)
        self.getCommandSet('plone').refreshPortlet(portlethash)
	mac = self.macroField(field='doczeichen', doczeichen=value)
        core = self.getCommandSet('core')
	core.replaceHTML(core.getHtmlIdSelector('archetypes-fieldname-doczeichen'), mac)

    @kssaction
    def listConstraint(self, masterid=None, value=None, form=None):
	v=""
        context = self.context
        dzu = getUtility(IDocZeichenUtility, name="nva.doczeichen.utility")
        core = self.getCommandSet('core')
	form = self.request.form
	#print value
	if masterid == "dz1":
	    v=form.get('dz1','')
            values = self._mkolist( dzu.getOG( v1=form.get('dz1')) )
	    htmlid = "dz2"
	elif masterid == "dz2":
	    v="%s" %(form.get('dz2',''))
            values = self._mkolist( dzu.getG( v1=form.get('dz1')[0], v2=form.get('dz2')[1] ))
	    htmlid = "dz3"
	elif masterid == "dz3":
	    v="%s" %(form.get('dz3',''))
	elif masterid == "dz4":
	    v="%s%s" %(form.get('dz3',''), form.get('dz4',''))
	elif masterid == "dz5":
	    v="%s%s%s" %(form.get('dz3',''), form.get('dz4',''), form.get('dz5',''))
	if masterid in ('dz1', 'dz2'):
	    sbox = "<select name='%s' id='%s'> %s </select>" %(htmlid, htmlid, ''.join(values))
	    core.replaceHTML(core.getHtmlIdSelector(htmlid), sbox)
	
	input = '<input type="text" name="ddzz" id="ddzz" value="%s" />' %v
	core.replaceHTML(core.getHtmlIdSelector('ddzz'), input)

    def _mkolist(self, values):
        rc=[]
        for value in values:
	    option='<option value="%s">%s</option>' %(value[0], value[1])
            rc.append(option)
	return rc

    def _mkolist3(self, values):
        rc=[] 
	context = self.context
	catalog = getToolByName(context,'portal_catalog')
        for value in values:
  	    docz = "%s*" %(value[0])
	    docz = docz.replace('.','')
	    if docz != '*':
#	        print "DokZ",  docz
                obj = catalog(searchdoczeichen = docz)
	        anzahl = len(obj)
	        option='<option value="%s">%s (%s)</option>' %(value[0], value[1], anzahl)
            else:
	        option='<option value="%s">%s</option>' %(value[0], value[1])
	    
            rc.append(option)
	return rc

    field_macros = ZopeTwoPageTemplateFile('field_wrapper.pt')
    def macroField(self, field, **kw):
        'Renders a given AT-Field and returns its text'
        self.request.form, orig_form = kw, self.request.form
	if kw.has_key('doczeichen'):
	   self.request['doczeichen'] = kw.get('doczeichen',[])
        content = self.field_macros(field=field)
        self.request.form = orig_form
        # Always encoded as utf-8
        try:
            content = force_unicode(content, 'utf-8')
        except:
            content = content
        return content

    @kssaction
    def listDoczeichen(self, masterid=None, value=None):
        context = self.context
        core = self.getCommandSet('core')
#	print "MasterID " , masterid
        dzu = getUtility(IDocZeichenUtility, name="nva.doczeichen.utility")
        if masterid == "dzv1":
            values = self._mkolist( dzu.getOG( v1=value) )
            htmlid = "dzv2"
        elif masterid == "dzv2":
            values = self._mkolist3( dzu.getG( v1=value[0], v2=value[1]) )
            htmlid = "dzv3"
        
        if masterid == "dzv1":
	    sbox = "<select name='%s' id='%s'> %s </select>" %(htmlid, htmlid, ''.join(values))
	    core.replaceHTML(core.getHtmlIdSelector(htmlid), sbox)
            htmlid = "dzv3"
	    sbox = "<select name='%s' id='%s'> %s </select>" %(htmlid, htmlid, '')
	    core.replaceHTML(core.getHtmlIdSelector(htmlid), sbox)
#            core.replaceInnerHTML(core.getHtmlIdSelector('dzv2'), 'Hallo World')
#	    print "dzv2 wurde erweitert"
        elif masterid == "dzv2":
	    sbox = "<select name='%s' id='%s'> %s </select>" %(htmlid, htmlid, ''.join(values))
	    core.replaceHTML(core.getHtmlIdSelector(htmlid), sbox)
#            core.replaceInnerHTML(core.getHtmlIdSelector('dzv3'), ''.join(values))
#	    print "dzv3 wurde erweitert"
	    
	catalog = getToolByName(context,'portal_catalog')
	docz = "%s*" %(value)
	docz = docz.replace('.','')
#	print "SearchValue", docz
        obj = catalog(searchdoczeichen = docz)
	html = self._mktable(obj)
	if html is not None:
	    html = force_unicode(html, 'utf')	
        core.replaceInnerHTML(core.getHtmlIdSelector('doczeichenresults'), html)

    def _mktable(self, obj):
	if len(obj) == 0:
            return "<h2> Keine Dokumente mit Ihren DOK-Zeichen gefunden </h2>"
        table = "<table class='listing'> <tr> <th> Title </th> <th> Beschreibung </th> <th> Datum </th> </tr> %s </table>"
        rc = []
        for x in obj:
	    s = "<tr> <td> <a href='%s'> %s </a> </td> <td> %s </td> <td> %s </td> </tr>" %(x.getURL(), x.Title, x.Description, x.ModificationDate)
            rc.append(s)
        return table %(''.join(rc))
