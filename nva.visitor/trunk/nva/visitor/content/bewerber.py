"""Definition of the Bewerber content type
"""

from zope.interface import implements
from Products.Archetypes.public import DisplayList
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from nva.visitor import visitorMessageFactory as _

from nva.visitor.interfaces import IBewerber
from nva.visitor.config import PROJECTNAME, branche, beziehung
from nva.visitor.lib.helpers import ldapsearch

from DateTime import DateTime

BewerberSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-


    atapi.StringField(
        'ortland',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Ort/Land"),
            description=_(u"Herkunft des Bewerbers (Ort/Land)"),
            size = 60,
        ),
        required=True,
    ),


    atapi.StringField(
        'ansprechpartner',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Wer"),
            description=_(u"Name des Bewerbers"),
            size = 60,
        ),
        required=True,
    ),


    atapi.DateTimeField(
        'startdate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(            label=_(u"Besuchsbeginn (Termin)"),
            description=_(u"Tragen Sie den vereinbarten Bessuchsbeginn ein oder klicken Sie auf das Kalender-Icon und treffen Sie eine Auswahl."),
        ),
        required=True,
        validators=('isValidDate'),
        default_method=DateTime,
    ),

    atapi.DateTimeField(
        'enddate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(            label=_(u"Besuchsende (Termin)"),
            description=_(u"Tragen Sie das vereinbarte Besuchsende ein oder klicken Sie auf das Kalender-Icon und treffen eine Auswahl."),
        ),
        required=True,
        validators=('isValidDate'),
        default_method=DateTime,
    ),

    atapi.TextField(
        'ablauf',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"zeitlicher Ablauf des Besuches"),
            description=_(u"Kurze Darstellung des zeitlichen Ablaufs."),
        ),
    ),

    atapi.StringField(
        'mylocation',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Ort"),
            description=_(u"Ort des Besuches"),
            size = 60,
        ),
        required=True,
    ),

    atapi.StringField(
        'grund',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Grund"),
            description=_(u"Grund des Besuches"),
        ),
        required=True,
        size = 60,
    ),

    atapi.TextField(
        'themen',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Themen"),
            description=_(u"Kurze Darstellung der Gespraechsthemen"),
        ),
        required=True,
    ),

    atapi.StringField(
        'contactname',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Kontaktperson"),
            description=_(u"Kontaktperson bei Pfister"),
        ),
    ),

    atapi.StringField(
        'contactphone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Kontakt Telefon"),
            description=_(u"Tragen Sie hier eine Telefonnummer ein, unter der man weitere Informationen anfordern oder buchen kann."),
        ),
        validators=('isInternationalPhoneNumber'),
    ),

    atapi.TextField(
        'gespraechsteilnehmer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Teilnehmer am Gespraech"),
            description=_(u"Namen der Gespraechsteilnehmer"),
        ),
        required=True,
    ),


    atapi.BooleanField(
        'mailsent',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"Mailinformation"),
            description=_(u"Ueber die Bewerberanmeldung wurde per Mail informiert."),
            visible = {'edit': False, 'view': False}
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

BewerberSchema['title'].storage = atapi.AnnotationStorage()
BewerberSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BewerberSchema, moveDiscussion=False)


class Bewerber(base.ATCTContent):
    """Anmeldung eines Bewerbers"""
    implements(IBewerber)

    meta_type = "Bewerber"
    schema = BewerberSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    mailsent = atapi.ATFieldProperty('mailsent')
    ortland = atapi.ATFieldProperty('ortland')
    ansprechpartner = atapi.ATFieldProperty('ansprechpartner')
    enddate = atapi.ATFieldProperty('enddate')
    startdate = atapi.ATFieldProperty('startdate')
    ablauf = atapi.ATFieldProperty('ablauf')
    mylocation = atapi.ATFieldProperty('mylocation')
    grund = atapi.ATFieldProperty('grund')
    themen = atapi.ATFieldProperty('themen')
    contactname = atapi.ATFieldProperty('contactname')
    contactphone = atapi.ATFieldProperty('contactphone')
    gespraechsteilnehmer = atapi.ATFieldProperty('gespraechsteilnehmer')


    def Besuchsbeginn(self):
        """Methode zum Indizieren des Besuchsbeginns"""
        return self.getStartdate()

    def Besuchsende(self):
        """Methode zum Indizieren des Besuchsendes"""
        return self.getEnddate()

    def Ort(self):
        """Methode zum Indizieren des besuchten Ortes"""
        return self.getMylocation()

    def Besucher(self):
        """Methode zum Indizieren des Besuchers"""
        return self.getAnsprechpartner()



atapi.registerType(Bewerber, PROJECTNAME)
