# -*- coding: utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from nva.tutorial.interfaces import ICheckHtml
from base64 import encodestring, decodestring
import urllib

class showHtml(api.View):
    api.context(Interface)

    def update(self):
        txt = self.request.get('txt', '')
        if txt:
            htmltxt = decodestring(txt)
            self.htmltxt = htmltxt.decode('utf-8')
        else:
            self.htmltxt = u'Leider konnte der HTML-Text nicht gelesen werden.'

    def render(self):
        mystring = self.htmltxt
        url = self.context.absolute_url()
        mytag = u'<p><a href="%s">zurück zum Tutorial</a></p>' %url
        if u'</body>' in mystring and u'</html>' in mystring:
            mystring = mystring.replace('</body>', mytag+'</body>')
        elif u'</body>' in mystring and not u'</html>' in mystring:
            mystring = mystring.replace(u'</body>', mytag+u'</body>')
        elif not u'</body>' in mystring and u'</html>' in mystring:
            mystring = mystring.replace(u'</html>', mytag+u'</html>')
        else:
            mystring = mystring + mytag
        return mystring

class CheckHtml(api.Form):
    """Form zum Test von HTML-Code"""
    api.context(Interface)
    fields = api.Fields(ICheckHtml)

    def validateHtml(self, value):
        from tidylib import tidy_document
        document, errors = tidy_document(value, options={'numeric-entities':1})
        if errors:
            self.context.plone_utils.addPortalMessage(u'Bitte prüfe Deinen HTML-Code anhand folgender Angaben %s'
                %errors, 'info')
            return True

    @api.action('HTML-Code testen')
    def handle_test(self):
        data, errors = self.extractData()
        if errors:
            return
        value = data.get('htmltext', '')
        moreerrors = self.validateHtml(value)
        #if moreerrors:
        #    return 
        htmltxt = data.get('htmltext', '').encode('utf-8')
        if htmltxt:
            htmltxt = encodestring(htmltxt)
            htmltxt = urllib.quote_plus(htmltxt)
            url = '%s/%s?txt=%s' %(self.url(), 'showhtml', htmltxt)
            return self.response.redirect(url)
        return
