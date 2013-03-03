# -*- coding: utf-8 -*-
"""Definition of the Fragestellung content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from nva.bsbetreuung import bsbetreuungMessageFactory as _

from nva.bsbetreuung.interfaces import IFragestellung
from nva.bsbetreuung.config import PROJECTNAME

FragestellungSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'hilfe',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Hilfetext"),
            description=_(u"Bitte beschreiben Sie hier eine Hilfe fuer diese Fragestellung."),
        ),
        default_output_type='text/html'
    ),


    atapi.FloatField(
        'faktor',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Faktor"),            description=_(u"Bitte tragen Sie hier einen Faktor fuer die Berechnung des Betreuungsaufwandes ein. Sind keine Antwortoptionen angegeben, gilt dieser Faktor fuer diese Fragestellung; die Fra
ge wird dann nicht eingeblendet. Sind dagegen Antwortoptionen angegeben, kann dieser Faktor als zusaetzlicher Gewichtungsfaktor genutzt werden."),
        ),
        required=True,
        default=_(u"1.0"),
        validators=('isDecimal'),
    ),


    atapi.TextField(
        'fieldtype',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Feldtyp"),
            description=_(u'Bitte wählen Sie hier die Art des Feldes aus. Bitte beachten Sie dabei, dass zur Berechnung des \
                            Betreuungsaufwandes nur Werte aus den Feldtypen "Auswahlfeld" und "Gleitkommazahl" berücksichtigt \
                            werden können. Die Feldtypen "Textzeile" und "Textblock" dienen der Kommentierung durch den \
                            Benutzer'),
        ),
        required=True,
        vocabulary=[('choice', 'Auswahlfeld'), ('float', 'Gleitkommazahl'),
                    ('textline', 'Textzeile'), ('text', 'Textblock')]
    ),


    atapi.LinesField(
        'optionen',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Optionen"),
            description=_(u"Bitte beschreiben Sie hier die Optionen fuer dieses Feld. Es gilt folgende Syntax: value|text. Beispiel: 1.0|mehr als 50% der Beschaeftigten. Bei Auswahl von Textfeld werden 
die Optionen ignoriert."),
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

FragestellungSchema['title'].storage = atapi.AnnotationStorage()
FragestellungSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(FragestellungSchema, moveDiscussion=False)


class Fragestellung(base.ATCTContent):
    """Fragestellung zu einer Aufgabe der betriebsspezifischen Betreuung"""
    implements(IFragestellung)

    meta_type = "Fragestellung"
    schema = FragestellungSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    fieldtype = atapi.ATFieldProperty('fieldtype')

    hilfe = atapi.ATFieldProperty('hilfe')

    faktor = atapi.ATFieldProperty('faktor')

    optionen = atapi.ATFieldProperty('optionen')

atapi.registerType(Fragestellung, PROJECTNAME)
