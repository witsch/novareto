# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class ProgressViewlet(ViewletBase):
    render = ViewPageTemplateFile('progress.pt')

    def update(self):

        fc = (self.context.aq_inner.aq_parent.listFolderContents())
        docindex = fc.index(self.context)

        ready = self.ready = docindex +1
        all = self.all = len(fc)
        self.rest = all - ready
