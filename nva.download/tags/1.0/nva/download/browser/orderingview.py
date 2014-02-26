# -*- coding: utf-8 -*-

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.download import downloadMessageFactory as _

class IorderingView(Interface):
    """
    ordering view interface
    """

    def test():
        """ test method"""


class orderingView(BrowserView):
    """
    ordering browser view
    """
    implements(IorderingView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}


    def order(self):
        myauswahl = []
        if isinstance(self.request.get('auswahl', ''), str):
            myauswahl.append(self.request.get('auswahl', ''))
        else: 
            myauswahl = self.request.get('auswahl', [])

        myChoice = '#'.join(myauswahl)
        table = """
                <table class="table table bordered">
                <tr><th>Pos.</th>
                    <th>Anzahl</th>
                    <th>Nr.</th>
                    <th>Titel</th></tr>
                """   
        count = 1
        for i in myauswahl:
            brains = self.portal_catalog.searchResults(UID = i)
            titel = brains[0].getObject().title
            id = brains[0].getObject().id
            row = """<tr><td>%s</td><td><input name="%s" type="text" value="1" size="2" maxlength="2">
                     </td><td>%s</td><td>%s</td></tr>""" % (count, i, id, titel)
            table += row
            count += 1
        table += '</table>'
        return {'choice':myChoice, 'table':table}
