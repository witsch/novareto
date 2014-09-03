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


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def refs(self, obj):
        """ returns a list of references """
        refs = [i.UID() for i in obj.getReferences('rel_titleimages')]
        brains = self.portal_catalog.searchResults(UID=refs, sort_on="Webcode")
        myrefs = []
        for i in brains:
            myrefs.append(i.getObject())
        return myrefs

    def update(self):
        self.imagelist = []
        self.videopath = None
        self.imagepath = None
        if self.context.portal_type in ['Folder', 'Document', 'Topic', 'Collection']:
            if getattr(self.context, 'anzeige', False):
                titelbilder = self.refs(self.context)
                if titelbilder:
                    to = len(titelbilder)
                    if getattr(self.context, 'zufall', False):
                        imageindex = random.randint(0, to-1)
                        randimage = titelbilder[imageindex]
                        refurl = ''
                        #Verlinkung des Titelbildes mit einem Inhalt
                        if randimage.getReferences():
                            refurl = randimage.getReferences()[0].absolute_url()
                        #Lesen des Titelbildes
                        if randimage.getField('image'):
                            image = {'img':randimage.getField('image').tag(randimage),
                                     'img-caption':randimage.title,
                                     'img-url': refurl}
                            self.imagelist.append(image)
                    else:
                        for i in range(to):
                            refurl = ''
                            #Verlinkung des Titelbildes mit einem Inhalt
                            if titelbilder[i].getReferences():
                                refurl = titelbilder[i].getReferences()[0].absolute_url()
                            if i == 0:
                                if titelbilder[i].getField('image'):
                                    image = {'data-slide':i, 
                                             'class':'active', 
                                             'item-class':'item active', 
                                             'img':titelbilder[i].getField('image').tag(titelbilder[i]),
                                             'img-caption':titelbilder[i].title,
                                             'img-url': refurl}
                                    self.imagelist.append(image)
                            else:
                                if titelbilder[i].getField('image'):
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
