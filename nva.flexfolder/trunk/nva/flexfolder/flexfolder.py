# -*- coding: utf-8 -*-
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from nva.flexfolder import MessageFactory as _


# Interface class; used to define content-type schema.

class IFlexfolder(form.Schema, IImageScaleTraversable):
    """
    Ein Ordner fuer die Anzeige von Inhalten, die via Webcode konfiguriert werden.
    """

    webcodes = schema.List(title=u"Liste der Webcodes",
                           description=u"Bitte tragen Sie hier die Liste mit den Webcodes der Inhalte ein,\
                           die in der Ordnerübersicht angezeigt werden sollen.",
                           value_type=schema.TextLine(required=True),
                           required = True,)

    order = schema.Bool(title=u"Webcocde-Inhalte vor den normalen Ordnerinhalten anzeigen.",
                           description=u"Bei Auswahl werden die Webcode-Inhalte vor dem Ordnerinhalt\
                           im anderen Fall danach.",
                           required = True,)

    text = RichText(title=u"Haupttext des Ordners",
                           required = False,)

class Flexfolder(Container):
    grok.implements(IFlexfolder)


    def getFolderContents(self, contentFilter=None,batch=False,b_size=100,full_objects=False):
        """Override Standard-Method"""

        mtool = self.portal_membership
        cur_path = '/'.join(self.getPhysicalPath())
        path = {}

        if not contentFilter:
            contentFilter = {}
        else:
            contentFilter = dict(contentFilter)

        if not contentFilter.get('sort_on', None):
            contentFilter['sort_on'] = 'getObjPositionInParent'

        if contentFilter.get('path', None) is None:
            path['query'] = cur_path
            path['depth'] = 1
            contentFilter['path'] = path

        show_inactive = mtool.checkPermission(
                        'Access inactive portal content', self)

        # Provide batching hints to the catalog
        b_start = int(self.REQUEST.get('b_start', 0))
        contentFilter['b_start'] = b_start
        if batch:
            contentFilter['b_size'] = b_size

        # Evaluate in catalog context because some containers override queryCatalog
        # with their own unrelated method (Topics)

        webcodes = None
        for i in self.webcodes:
            brains = self.portal_catalog(Webcode=i)
            if brains and not webcodes:
                webcodes = brains
            elif brains and webcodes:
                webcodes = webcodes + brains

        contents = self.portal_catalog.queryCatalog(contentFilter, show_all=1,
                                                    show_inactive=show_inactive, )

        if webcodes and self.order:
            contents = webcodes + contents
        else:
            contents = contents + webcodes

        if full_objects:
            contents = [b.getObject() for b in contents]

        if batch:
            from Products.CMFPlone import Batch
            batch = Batch(contents, b_size, b_start, orphan=0)
            return batch

        return contents

class SampleView(grok.View):
    """ sample view class """

    grok.context(IFlexfolder)
    grok.require('zope2.View')

