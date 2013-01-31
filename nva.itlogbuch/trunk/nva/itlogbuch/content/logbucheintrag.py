"""Definition of the Logbucheintrag content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from DateTime.DateTime import DateTime

# -*- Message Factory Imported Here -*-

from nva.itlogbuch.interfaces import ILogbucheintrag
from nva.itlogbuch.config import PROJECTNAME
from nva.itlogbuch import itlogbuchMessageFactory as _

LogbucheintragSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'mitarbeiter',
        storage=atapi.AnnotationStorage(),
        default_method = 'getDefaultMitarbeiter',
        widget=atapi.StringWidget(
            label=_(u"Mitarbeiter"),
            description=_(u"Bitte tragen Sie hier den fuer die Aenderung verantwortlichen Mitarbeiter ein."),
        ),
        required=True,
    ),


    atapi.StringField(
        'description',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Description"),
            condition = "python: False",
            ),
        ),


    atapi.DateTimeField(
        'aenderungsdatum',
        storage=atapi.AnnotationStorage(),
        default_method = 'getDateTimeDefault',
        widget=atapi.CalendarWidget(
            label=_(u"Aenderungsdatum / Uhrzeit"),
            description=_(u"Bitte tragen Sie hier ein, zu welchem Datum und welcher Uhrzeit die von Ihnen durchgefuehrte Aenderung wirksam wurde bzw. wird."),
        ),
        required=True,
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'systemkategorie',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Systemkategorie"),
            description=_(u"Bitte waehlen Sie aus, fuer welche Systemkategorie die Aenderung durchgefuehrt wurde."),
        ),
        required=True,
        vocabulary_factory = "SYSTEMVOCAB",
    ),


    atapi.StringField(
        'aenderungskategorie',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Aenderungskategorie"),
            description=_(u"Bitte waehlen Sie aus, welcher Kategorie die Aenderung zugeordnet werden kann."),
        ),
        required=True,
        vocabulary_factory = "AENDERUNGVOCAB",
    ),


    atapi.TextField(
        'aenderungen',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Aenderungen"),
            description=_(u"Bitte beschreiben Sie hier die von Ihnen durchgefuehrten Aenderungen."),
        ),
        required=True,
    ),

    atapi.StringField(
        'inetticket',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Inet Ticketnummer"),
            description=_(u"Hier koennen Sie eine Referenz  zu einem INet-Ticket eintragen falls ein solches existiert."),
        ),
        required=True,
    ),

    atapi.StringField(
        'projektnummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Projektnummer"),
            description=_(u"Bitte geben Sie hieer, wenn vorhanden, die Nummer des IT-Projektes an fuer die Sie die Aenderung durchgefuehrt haben."),
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

LogbucheintragSchema['title'].storage = atapi.AnnotationStorage()
LogbucheintragSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(LogbucheintragSchema, moveDiscussion=False)


class Logbucheintrag(base.ATCTContent):
    """Eintrag im Logbuch"""
    implements(ILogbucheintrag)

    meta_type = "Logbucheintrag"
    schema = LogbucheintragSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def getDateTimeDefault(self):
        return DateTime()

    def getDefaultMitarbeiter(self):
        pm = getToolByName(self, 'portal_membership')
        user = pm.getAuthenticatedMember()
        return user.getProperty('fullname')

atapi.registerType(Logbucheintrag, PROJECTNAME)
