import random
import urllib
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from datetime import datetime, timedelta
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import ics

def iso2german(s):
    """ Convert YYYY-MM-DD to DD.MM.YYYY"""
    fields = s.split('-')
    return '%s.%s.%s' % (fields[-1], fields[1], fields[0])

class Orders(BrowserView):

    def getDateRange(self, start_date=None, start_offset_days=14, num_days=30):
        """ Calculate the day range for the matrix based on a given 'start_date'
            or <current date> + <start_offset_days> (2 weeks by default)

        """
        if not start_date:
            start_date = datetime.now() + timedelta(days=start_offset_days)
        return ics.getDateRange(start_date, num_days)

    def getItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'portal_type' : ['nva.borrow.borrowableitem']})
        objs = [brain.getObject() for brain in brains]
        category = self.request.get('category')
        if category:
            objs = [o for o in objs if category in o.categories]
        return objs

    def getItemIds(self):
        return [item.restrictedTraverse('@@getIntId')() for item in self.getItems()]

    def random(self, upper=1):
        return random.randint(0, upper)

    def showBestellung(self):
        """ Return a HTML snippet for request/items to be injected through
            an PFG overrides configuration inside for the 'bestellung' 
            RichLabelField.
        """
        intidutil = getUtility(IIntIds)
        html = list()
        html.append('<ul id="bestellung">')
        import pdb; pdb.set_trace() 
        for d in eval(self.request.form.get('formData', {})).get('items', []):
            obj = intidutil.getObject(int(d['id']))
            number = int(d['number'])
            html.append('<li>%d x %s</li>' % (number, obj.Title()))
        html.append('</ul>')
        return u''.join(html)

    def processBooking(self):
        buchungStart = iso2german(self.request.form['dates'][0])
        buchungEnde = iso2german(self.request.form['dates'][-1])

        # Pass some hidden/read-only parameters to the PFG form
        params = {'buchungStart' : buchungStart,
                  'buchungEnde' : buchungEnde,
                  'formData' : str(self.request.form)    
                }
        self.request.response.redirect('%s/order-form?%s' % 
                                       (self.context.absolute_url(), urllib.urlencode(params)))

