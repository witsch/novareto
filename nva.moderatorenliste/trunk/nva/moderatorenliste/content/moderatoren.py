"""Definition of the Moderatoren content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from nva.moderatorenliste import moderatorenlisteMessageFactory as _
from nva.moderatorenliste.interfaces import IModeratoren
from nva.moderatorenliste.config import PROJECTNAME

ModeratorenSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-



    atapi.StringField(
        'mitgliedsnummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Mitgliedsnummer"),
            description=_(u"Bitte geben Sie hier die Mitgliedsnummer ein."),
        ),
        required=True,
    ),

    atapi.StringField(
        'name',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Name"),
            description=_(u"Name"),
        ),
    ),

    atapi.StringField(
        'vorname',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Vorname"),
            description=_(u"Vorname"),
        ),
    ),

    atapi.StringField(
        'strassenr',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Strasse, Hausnummer"),
            description=_(u"Strasse Hausnummer"),
        ),
    ),

    atapi.StringField(
        'plz',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Postleitzahl"),
            description=_(u"Postleitzahl"),
        ),
    ),

    atapi.StringField(
        'ort',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Ort"),
            description=_(u"Ort"),
        ),
    ),

    atapi.StringField(
        'telefonnummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Telefonnummer"),
            description=_(u"Telefonnummer"),
        ),
    ),

    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"E-Mail Adresse"),
            description=_(u"E-Mail Adresse"),
        ),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ModeratorenSchema['title'].storage = atapi.AnnotationStorage()
ModeratorenSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ModeratorenSchema, moveDiscussion=False)

class Moderatoren(base.ATCTContent):
    """Moderatoren"""
    implements(IModeratoren)

    meta_type = "Moderatoren"
    schema = ModeratorenSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    name = atapi.ATFieldProperty('name')

    mitgliedsnummer = atapi.ATFieldProperty('mitgliedsnummer')


atapi.registerType(Moderatoren, PROJECTNAME)
