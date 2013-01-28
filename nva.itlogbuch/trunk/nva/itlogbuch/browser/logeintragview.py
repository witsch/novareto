import string
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.itlogbuch import itlogbuchMessageFactory as _


class IlogeintragView(Interface):
    """
    logeintrag view interface
    """

    def test():
        """ test method"""


class logeintragView(BrowserView):
    """
    logeintrag browser view
    """
    implements(IlogeintragView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def data(self):
        """
        renders data for logentry
        """
        data = {}
        data['mitarbeiter'] = self.context.getMitarbeiter()
        data['aenderungsdatum'] = self.context.toLocalizedTime(self.context.getAenderungsdatum(), long_format=True) + ' Uhr'
        data['systemkategorie'] = self.context.getSystemkategorie()
        data['aenderungskategorie'] = string.join(self.context.getAenderungskategorie(), ',')
        data['aenderungen'] = self.context.getAenderungen()
        data['inetticket'] = self.context.getInetticket()
        data['ticket_url'] = 'http://debaw2s450/helpdesk/scripts/main.asp?ticketid=%s' % self.context.getInetticket()
        data['projektnummer'] = self.context.getProjektnummer()
        return data
