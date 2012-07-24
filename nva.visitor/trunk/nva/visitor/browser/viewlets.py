# -*- coding: utf-8 -*-
import Acquisition
from zope.component import getMultiAdapter, queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class MyVisitorActionsViewlet(ViewletBase):

    index = ViewPageTemplateFile("visitor_actions.pt")

    def update(self):
        super(MyVisitorActionsViewlet, self).update()
    
        mytype = False
        if self.context.portal_type == "Besuchsanmeldung":
            mytype = True
        self.hasRightType = mytype

        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.sent = self.context.mailsent

    def hasRightRoles(self):
        pm = getToolByName(self.context, 'portal_membership')
        userRoles = pm.getAuthenticatedMember().getRoles()
        rightRoles = ['Manager', 'Owner']
        compare = set(userRoles) & set(rightRoles)
        if compare:
            return True
        return False


    def toLocalizedTime(self, time, long_format=None, time_only = None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        return util.ulocalized_time(time, long_format, time_only, self.context,
                                    domain='plonelocales')

    def getWebcode(self):
        """Holt den Webcode fuer den Inhalt"""
        try:
            webcode = self.context.webcode
        except:
            webcode = ''
        return webcode

