# -*- coding: utf-8 -*-
from five import grok
import random
from time import strftime, localtime
from DateTime import DateTime
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder, IContextAwareDefaultFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFCore.utils import getToolByName
from bgetem.praevention import MessageFactory as _
from Products.ATContentTypes.interfaces import IATImage

@grok.provider(IContextAwareDefaultFactory)
def genWebcode(context):
    aktuell=unicode(DateTime()).split(' ')[0]
    neujahr='%s/01/01' %str(DateTime()).split(' ')[0][:4]
    konstante=unicode(aktuell[2:4])
    zufallszahl=unicode(random.randint(100000, 999999))
    code=konstante+zufallszahl
    pcat=getToolByName(context,'portal_catalog')
    results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
    while results:
        zufallszahl=unicode(random.randint(100000, 999999))
        code=konstante+zufallszahl
        results = pcat(Webcode=code, created={"query":[neujahr,aktuell],"range":"minmax"})
    return code

class IDokuPraevention(form.Schema, IImageScaleTraversable):
    """
    Artikeltyp zur Erfassung von Dokumentationen im Bereich Praevention der BG ETEM.
    """

    haupttext = RichText(
                title=u"Haupttext",
                description=u"Bitte schreiben Sie hier den Haupttext Ihrer Dokumentation. Bitte fertigen Sie möglichst\
                            fein granulare Textbausteine Ihres Inhalts an. Die endgültige Dokumentation wird später\
                            aus mehrern dieser Textbausteine zusammengesetzt.",
                required = True,
                )

    details = RichText(
              title=u"Details",
              description=u"In diesem Bereich können sie für die Benutzer wertvolle Zusatzinformationen bereitstellen,\
                          die den Lesern bei Bedarf oder weitergehendem Interesse per Mausklick angezeigt\
                          werden.",
              required = False,
              )

    bilder = RelationChoice(
              title=u"Bildreferenzen",
              description=u"Bitte wählen Sie hier aus, welche Bilder im Zusammenhang mit dem Inhalt angezeigt\
                          werden sollen. Die Bilder werden jedoch nicht als Bestandteil des Haupttextes\
                          angezeigt.",
              source=ObjPathSourceBinder(object_provides=IATImage.__identifier__),
              required=False,
              )

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

    webcode = schema.TextLine(
              title=u"Webcode",
              description=u"Der Webcode für diesen Artikel wird automatisch errechnet und angezeigt. Sie\
                          können diesen Webcode bei Bedarf jedoch jederzeit überschreiben.",
              required = True,
              defaultFactory = genWebcode,
              )

class DokuPraevention(Container):
    grok.implements(IDokuPraevention)

    def getWebcode(self):
        """Emulate a Archetypes Accessor"""
        return self.webcode

class SampleView(grok.View):
    """ sample view class """

    grok.context(IDokuPraevention)
    grok.require('zope2.View')

    # grok.name('view')
    # Add view methods here
