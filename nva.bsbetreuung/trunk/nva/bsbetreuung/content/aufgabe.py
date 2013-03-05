# -*- coding: utf-8 -*-
"""Definition of the Aufgabe content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from nva.bsbetreuung import bsbetreuungMessageFactory as _

from nva.bsbetreuung.interfaces import IAufgabe
from nva.bsbetreuung.config import PROJECTNAME

AufgabeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'nummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Nummer des Aufgabenfeldes"),
            description=_(u"Unter dieser Nummer werden die Benutzereingaben fuer dieses Aufgabenfeld gespeichert."),
        ),
        required=True,
    ),


    atapi.TextField(
        'aufgabentext',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Aufgabentext"),
            description=_(u"Bitte beschreiben Sie hier die Aufgabe."),
        ),
        required=True,
        default_output_type='text/html',
    ),


    atapi.TextField(
        'hilfe',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Hilfetext"),
            description=_(u"Bitte machen Sie hier eine Eingabe, wenn Sie zusaetzliche Hilfestellung fuer ddieses Aufgabengebiet anbieten wollen."),
            rows = 5,
        ),
        default_output_type='text/html'
    ),


    atapi.FloatField(
        'basiszeitfaktor',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Basiszeitfaktor"),
            description=_(u"Bitte geben Sie in Stunden/Jahr an, welcher Basiszeitfaktor fuer dieses Aufgabenfeld gelten soll."),
        ),
        required=True,
        default=_(u"0.05"),
        validators=('isDecimal'),
    ),


    atapi.FloatField(
        'minimum',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Minimum Stunden/Jahr"),
            description=_(u"Bitte geben Sie hier an, welcher minimale Aufwand in Stunden/Jahr fuer dieses Aufgabenfeld gelten soll."),
        ),
        default=_("1.0"),
        validators=('isDecimal'),
    ),


    atapi.FloatField(
        'maximum',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Maximum Stunden/Jahr"),
            description=_(u"Bitte geben Sie hier den Maximalwert in Stunden/Jahr fuer dieses Aufgabenfeld  ein."),
        ),
        validators=('isDecimal'),
    ),


    atapi.StringField(
        'alternativtext',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Alternativtext"),
            description=_(u"Der Alternativtext wird eingeblendet, wenn Sie keine Fragestellungen zu diesem Feld ausgewaehlt haben."),
        ),
    ),


    atapi.ReferenceField(
        'fragen',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Fragestellungen"),
            description=_(u"Bitte waehlen Sie aus, welche Fragestellungen Ihrer Aufgabe zugeordnet werdenn  sollen."),
            allow_search=True,
        ),
        relationship='aufgabe_fragen',
        allowed_types=('Fragestellung',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'startend',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Weiterleitung"),
            description=_(u"Auf der ersten Seite des Wizards bitte hier auf die Einleitung referenzieren, auf der \
                            letzten Seite des Wizards auf die Seite mit der Ergebnisuebersicht"),
        ),
        relationship='aufgabe_startend',
        multiValued=True,
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

AufgabeSchema['title'].storage = atapi.AnnotationStorage()
AufgabeSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(AufgabeSchema, moveDiscussion=False)


class Aufgabe(base.ATCTContent):
    """Aufgabe in der betriebbspezifischen Betreuung"""
    implements(IAufgabe)

    meta_type = "Aufgabe"
    schema = AufgabeSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    nummer = atapi.ATFieldProperty('nummer')

    aufgabentext = atapi.ATFieldProperty('aufgabentext')

    hilfe = atapi.ATFieldProperty('hilfe')

    basiszeitfaktor = atapi.ATFieldProperty('basiszeitfaktor')

    minimum = atapi.ATFieldProperty('minimum')

    maximum = atapi.ATFieldProperty('maximum')

    alternativtext = atapi.ATFieldProperty('alternativtext')

    fragen = atapi.ATReferenceFieldProperty('fragen')

    startend = atapi.ATReferenceFieldProperty('startend')

atapi.registerType(Aufgabe, PROJECTNAME)
