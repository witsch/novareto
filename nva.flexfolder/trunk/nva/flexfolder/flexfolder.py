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

from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

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

    documentorder = schema.Bool(title = u"Ordner vor Dokumenten anzeigen",
                           description = u"Bei Auswahl werden die ordnerähnlichen Objekte vor normalen\
                           Objekten (Dokument, Seite) angezeigt, im anderen Fall danach.",
                           default = True,
                           required = True,)

    text = RichText(title=u"Haupttext des Ordners",
                           required = False,)

    titelbilder = RelationList(title=u"Titelbilder",
                           description=u"Hier können Sie Titelbilder für die Anzeige im Kopf der Seite auswählen",
                           default=[],
                           value_type=RelationChoice(title=_(u"Titelbilder"),
                                                     source=ObjPathSourceBinder()),
                           required=False,)

    anzeige = schema.Bool(title=u"Anzeige des Titelbildes im Ordner.",
                          default = True,
                          required = False,)

    spalte = schema.Bool(title=u"Anzeige des Titelbildes in der Zweispaltenansicht.",
                         default = True,
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

        webcodes = self.portal_catalog(Webcode=self.webcodes)

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

