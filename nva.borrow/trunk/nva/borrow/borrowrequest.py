from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from nva.borrow import MessageFactory as _

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from borrowableitem import IBorrowableItem


class IBorrowRequest(form.Schema, IImageScaleTraversable):
    """
    Request to borrow items
    """

    unternehmen = schema.TextLine(
        title=_(u'Unternehmen'),
        required=True,
        default=u'')   

    mitgliedsnr = schema.TextLine(
        title=_(u'Mitgliedsnummer'),
        required=True,
        default=u'')   

    vorname = schema.TextLine(
        title=_(u'Vorname'),
        required=True,
        default=u'')   
    nachname = schema.TextLine(
        title=_(u'Nachname'),
        required=True,
        default=u'')   
    email = schema.TextLine(
        title=_(u'Email'),
        required=True,
        default=u'')   
    telefon = schema.TextLine(
        title=_(u'Telefon'),
        required=True,
        default=u'')   
    fax = schema.TextLine(
        title=_(u'Fax'),
        required=True,
        default=u'')   

    adresse = schema.TextLine(
        title=_(u'Adresse'),
        required=True,
        default=u'')   
    adresse2 = schema.TextLine(
        title=_(u'Adresszusatz'),
        required=True,
        default=u'')   
    plz = schema.TextLine(
        title=_(u'Stadt'),
        required=True,
        default=u'')   
    lieferzeit = schema.TextLine(
        title=_(u'Lieferzeit'),
        required=True,
        default=u'')   
    besucherzahl = schema.TextLine(
        title=_(u'Besucherzahl'),
        required=True,
        default=u'')   

    thema = schema.TextLine(
        title=_(u'Thema'),
        required=True,
        default=u'')   

    formData = schema.TextLine(
        title=_(u'Form data'),
        required=True,
        default=u'')   

    buchungStart = schema.Date(
        title=_(u'Buchung von'),
        required=True,
        default=None)

    buchungStart = schema.Date(
        title=_(u'Buchung bis'),
        required=True,
        default=None)

    @invariant
    def validateStartEnd(data):
        if data.buchungStart is not None and data.buchungEnde is not None:
            if data.buchungStart > data.buchungEnde:
                raise Invalid(_(u"The start date must be before the end date."))

class BorrowRequest(dexterity.Item):
    grok.implements(IBorrowRequest)

    def Title(self):
        """ Return computed title """
        return '[Buchung] %s: %s - %s' % (self.unternehmen, self.buchungStart, self.buchungEnde)
    

class SampleView(grok.View):
    grok.context(IBorrowRequest)
    grok.require('zope2.View')
    
