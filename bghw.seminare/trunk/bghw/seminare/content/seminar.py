# -*- coding: utf-8 -*-
"""Definition of the Seminar content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from bghw.seminare import seminareMessageFactory as _

from bghw.seminare.interfaces import ISeminar
from bghw.seminare.config import PROJECTNAME

SeminarSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Haupttext zum Seminar"),
            description=_(u"Bitte beschreiben Sie hier aausfuehrlich das angebotene Seminar."),
            rows = 30,
        ),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
    ),


    atapi.ReferenceField(
        'aform',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Auswahl des Anmeldeformulars"),
            description=_(u"Bitte waehlen Sie hier aus, welches Anmeldeformular verwendet werden soll."),
        ),
        relationship='seminar_anmeldeformular',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.TextField(
        'prerequisites',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Voraussetzungen fuer die Teilnahme"),
            description=_(u"Geben Sie hier die notwendigen Voraussetzungen fuer die Teilnahme an."),
            rows = 10,
        ),
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
    ),


    #atapi.StringField(
    #    'veranstalter',
    #    storage=atapi.AnnotationStorage(),
    #    widget=atapi.SelectionWidget(
    #        label=_(u"Seminarveranstalter"),
    #        description=_(u"Bitte waehlen Sie aus, welche Sparte dieses Seminar anbietet."),
    #    ),
    #    required=True,
    #),


    atapi.StringField(
        'contactName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Ansprechpartner"),
            description=_(u"Bitte tragen Sie hier den Ansprechpartner der BGHW ein."),
        ),
        required=True,
    ),


    atapi.StringField(
        'contactEmail',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"E-Mail"),
            description=_(u"Mailadresse des Ansprechpartners."),
        ),
        required=True,
        validators = ('isEmail',),
    ),


    atapi.StringField(
        'contactPhone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Telefon"),
            description=_(u"Telefonnummer des Ansprechpartners."),
        ),
        required=True,
    ),


    atapi.StringField(
        'contactFax',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Telefax"),
            description=_(u"Telefaxnummer des Ansprechpartners."),
        ),
    ),


    atapi.ReferenceField(
        'referenz',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Abschlusseiten"),
            description=_(u"Waehlen Sie hier geeignete Artikel, die nacheinander zum Abschluss der Anmeldung angezeigt werden."),
            allow_search = True,
            allow_browser = True,
            show_indexes = False,
            force_close_on_insert = True,
        ),
        relationship='seminar_referenz',
        allowed_types=('Document', 'News Item', 'Event', 'Map',),
        multiValued=True,
    ),


    atapi.StringField(
        'exturl',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Externe URL"),
            description=_(u"Bitte geben Sie hier eine externe URL an, auf die fuer die Seminaranmeldung verwiesen werden soll"),
        ),
    ),


    atapi.StringField(
        'serviceid',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Webservic-ID"),
            description=_(u"Bitte geben Sie hier die Parameter fuer den Aufruf des BGHW-Webservice an."),
        ),
    ),


    atapi.FileField(
        'datefile',
        storage = atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Termindatei"),
            description=_(u"Hier koennen Sie eine Datei mit Seminarterminen hochladen."),
        ),
        validators=('isNonEmptyFile'),
        required = True,
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SeminarSchema['title'].storage = atapi.AnnotationStorage()
SeminarSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SeminarSchema, moveDiscussion=False)


class Seminar(base.ATCTContent):
    """Beschreibung der Eigenschaften des SSeminars"""
    implements(ISeminar)

    meta_type = "Seminar"
    schema = SeminarSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    text = atapi.ATFieldProperty('text')

    aform = atapi.ATReferenceFieldProperty('aform')

    prerequisites = atapi.ATFieldProperty('prerequisites')

    #veranstalter = atapi.ATFieldProperty('veranstalter')

    contactName = atapi.ATFieldProperty('contactName')

    contactEmail = atapi.ATFieldProperty('contactEmail')

    contactPhone = atapi.ATFieldProperty('contactPhone')

    contactFax = atapi.ATFieldProperty('contactFax')

    referenz = atapi.ATReferenceFieldProperty('referenz')

    exturl = atapi.ATFieldProperty('exturl')

    serviceid = atapi.ATFieldProperty('serviceid')

    datefile = atapi.ATFieldProperty('datefile')


atapi.registerType(Seminar, PROJECTNAME)
