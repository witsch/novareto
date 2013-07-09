# -*- coding: utf-8 -*-
# Copyright (c) 2004-2009 novareto GmbH
# lwalther@novareto.de
import string
import datetime
import random
from time import time
import Acquisition
from zope.component import getMultiAdapter, queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram

from nva.titelbild import titelbildMessageFactory as _

def getMediaButtons(background):
    if background[0] == 'light':
        return ('button_imagelink_light.png', 'button_videolink_light.png')
    else:
        return ('button_imagelink_dark.png', 'button_videolink_dark.png')

class TitleImageViewlet(ViewletBase):
    render = ViewPageTemplateFile('titelbild.pt')

    def update(self):
        self.imagelist = []
        self.videopath = None
        self.imagepath = None
        if self.context.portal_type in ['Folder', 'Document', 'Topic', 'Collection']:
            if getattr(self.context, 'anzeige', False):
                titelbilder = self.context.getReferences('rel_titleimages')
                if titelbilder:
                    if getattr(self.context, 'zufall', False):
                        to = len(titelbilder)
                        imageindex = random.randint(0, to-1)
                        randimage = titelbilder[imageindex]
                        self.imagelist.append(randimage.getField('image').tag(randimage))
                        if self.context.getReferences('rel_videopath'):
                            self.videopath = self.context.getReferences('rel_videopath')[0].absolute_url()
                            self.videobutton = getMediaButtons(getattr(self.context, 'background'))[1]
                        if self.context.getReferences('rel_imagepath'):
                            self.imagepath = self.context.getReferences('rel_imagepath')[0].absolute_url()
                            self.imagebutton = getMediaButtons(getattr(self.context, 'background'))[0]
                    else:
                        for i in titelbilder:
                            self.imagelist.append(i.getField('image').tag(i))
        #elif self.context.portal_type in ['GeoLocation',]:
        #    if getattr(self.context, 'anzeige', False):
        #        if getattr(self.context, 'folderimage', None):
        #            self.imagelist.append(str(self.context.folderimage))
        return
