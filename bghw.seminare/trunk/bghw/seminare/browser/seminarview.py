# -*- coding:utf-8 -*-
from zope.interface import implements, Interface
from xlrd import open_workbook

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from bghw.seminare import seminareMessageFactory as _


class IseminarView(Interface):
    """
    seminar view interface
    """

    def test():
        """ test method"""


class seminarView(BrowserView):
    """
    seminar browser view
    """
    implements(IseminarView)

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


    def getTableData(self):
        """
        returns the table data
        """
        fo = self.context.datefile
        wb = open_workbook(file_contents = str(fo))
        terminsheet = wb.sheet_by_name('termine')
        try:
            plzsheet = wb.sheet_by_name('plz')
        except:
            plzsheet = None

        print terminsheet
        print plzsheet

