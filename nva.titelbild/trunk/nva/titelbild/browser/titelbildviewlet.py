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
                    to = len(titelbilder)
                    if getattr(self.context, 'zufall', False):
                        imageindex = random.randint(0, to-1)
                        randimage = titelbilder[imageindex]
                        refurl = ''
                        if randimage.getReferences()
                            refurl = randimage.getReferences()[0].absolute_url()
                        image = {'img':randimage.getField('image').tag(randimage),
                                 'img-caption':randimage.title,
                                 'img-url': refurl}
                        self.imagelist.append(image)
                    else:
                        for i in range(to):
                            refurl = ''
                            if titelbilder[i].getReferences():
                                refurl = titelbilder[i].getReferences()[0].absolute_url()
                            if i == 0:
                                image = {'data-slide':i, 
                                         'class':'active', 
                                         'item-class':'item active', 
                                         'img':titelbilder[i].getField('image').tag(titelbilder[i]),
                                         'img-caption':titelbilder[i].title,
                                         'img-url': refurl}
                                self.imagelist.append(image)
                            else:
                                image = {'data-slide':i, 
                                         'class':'', 
                                         'item-class':'item', 
                                         'img':titelbilder[i].getField('image').tag(titelbilder[i]),
                                         'img-caption':titelbilder[i].title,
                                         'img-url': refurl}
                                self.imagelist.append(image)
                    if self.context.getReferences('rel_videopath'):
                        self.videopath = self.context.getReferences('rel_videopath')[0].absolute_url()
                    if self.context.getReferences('rel_imagepath'):
                        self.imagepath = self.context.getReferences('rel_imagepath')[0].absolute_url()

        return
