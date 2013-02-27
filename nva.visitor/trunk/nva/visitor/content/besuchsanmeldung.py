# -*- coding: utf-8 -*-
"""Definition of the Besuchsanmeldung content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from nva.visitor import visitorMessageFactory as _

from nva.visitor.interfaces import IBesuchsanmeldung
from nva.visitor.config import PROJECTNAME, branche, beziehung
from nva.visitor.lib.helpers import ldapsearch

from DateTime import DateTime

BesuchsanmeldungSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'firma',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Firma"),
            description=_(u"Firmenname des Besuchers"),
            size = 60,
        ),
        required=True,
    ),


    atapi.StringField(
        'ortland',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Ort/Land"),
            description=_(u"Herkunft des Besuchers (Ort/Land)"),
            size = 60,
        ),
        required=True,
    ),


    atapi.LinesField(
        'brancheaktivitaeten',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Branche"),
            description=_(u"Auswahl der Branche / Aktivitaeten des Besuchers"),
        ),
        required=True,
        vocabulary = branche,
    ),


    atapi.LinesField(
        'gbeziehung',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Geschaeftsbeziehung"),
            description=_(u"Auswahl der Art der Geschaeftsbeziehung"),
        ),
        required=True,
        vocabulary = beziehung, 
    ),


    atapi.StringField(
        'ansprechpartner',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Ansprechpartner"),
            description=_(u"Name des Besuchers / Ansprechpartners"),
            size = 60,
        ),
        required=True,
    ),


    atapi.StringField(
        'funktion',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Funktion"),
            description=_(u"Funktion des Besuchers / Ansprechpartners"),
            size = 60,
        ),
        required=True,
    ),


    atapi.DateTimeField(
        'startdate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Besuchsbeginn (Termin)"),
            description=_(u"Tragen Sie den vereinbarten Bessuchsbeginn ein oder klicken Sie auf das Kalender-Icon und treffen eine Auswahl."),
        ),
        required=True,
        validators=('isValidDate'),
        default_method=DateTime,
    ),


    atapi.DateTimeField(
        'enddate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Besuchsende (Termin)"),
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


    atapi.StringField(
        'mailing',
        storage=atapi.AnnotationStorage(),
        widget=atapi.MultiSelectionWidget(
            label=_(u"zusaetzlich per E-Mail informieren"),
            description=_(u"Hier koennen Empfaenger ausgewaehlt werden, die per E-Mail ueber den Termin benachrichtigt werden sollen. Mitglieder der Geschaeftsfuehrung und die Pforte werden immer informiert."),
            size = 20,
        ),
        vocabulary="adsearchliste",
    ),

    atapi.BooleanField(
        'mailsent',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"Mailinformation"),
            description=_(u"Ueber die Besuchsanmeldung wurde per Mail informiert."),
            visible = {'edit': False, 'view': False}
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

BesuchsanmeldungSchema['title'].storage = atapi.AnnotationStorage()
BesuchsanmeldungSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BesuchsanmeldungSchema, moveDiscussion=False)


class Besuchsanmeldung(base.ATCTContent):
    """Spezielle Form eines Termins zur Anmeldung von Besuchern im Intranet."""
    implements(IBesuchsanmeldung)

    meta_type = "Besuchsanmeldung"
    schema = BesuchsanmeldungSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    mailsent = atapi.ATFieldProperty('mailsent')
    firma = atapi.ATFieldProperty('firma')
    ortland = atapi.ATFieldProperty('ortland')
    brancheaktivitaeten = atapi.ATFieldProperty('brancheaktivitaeten')
    gbeziehung = atapi.ATFieldProperty('gbeziehung')
    ansprechpartner = atapi.ATFieldProperty('ansprechpartner')
    funktion = atapi.ATFieldProperty('funktion')
    enddate = atapi.ATFieldProperty('enddate')
    startdate = atapi.ATFieldProperty('startdate')
    ablauf = atapi.ATFieldProperty('ablauf')
    mylocation = atapi.ATFieldProperty('mylocation')
    grund = atapi.ATFieldProperty('grund')
    themen = atapi.ATFieldProperty('themen')
    contactname = atapi.ATFieldProperty('contactname')
    contactphone = atapi.ATFieldProperty('contactphone')
    gespraechsteilnehmer = atapi.ATFieldProperty('gespraechsteilnehmer')
    mailing = atapi.ATFieldProperty('mailing')

    def adsearchliste(self):
        """ Suche im AD-Verzeichnis"""
        res = ldapsearch()
        liste=[]
        if res:
            for entry in res:
                attr = entry[1]
                if attr.has_key('mail'):
                    if attr.has_key('msExchHideFromAddressLists'):
                        verstecken=attr['msExchHideFromAddressLists']
                        if verstecken == ['FALSE']:
                            eintrag=[attr['name'][0],attr['mail'][0]]
                            liste.append(eintrag)
                    else:
                        eintrag=[attr['name'][0],attr['mail'][0]]
                        liste.append(eintrag)
        liste.sort()
        results=[]
        for x in liste:
                if not x[0].startswith('AGB-'):
                    results.append([x[1],x[0]])
        mailtuple=tuple(results)
        return DisplayList(mailtuple)

    def Besuchsbeginn(self):
        """Methode zum Indizieren des Besuchsbeginns"""
        return self.getStartdate()

    def Besuchsende(self):
        """Methode zum Indizieren des Besuchsendes"""
        return self.getEnddate()

    def Lokation(self):
        """Methode zum Indizieren des besuchten Ortes"""
        return self.getMylocation()

    def Besucher(self):
        """Methode zum Indizieren des Besuchers"""
        return self.getAnsprechpartner()

    def Firma(self):
        """Methode zum Indizieren der Firma"""
        return self.getFirma()

atapi.registerType(Besuchsanmeldung, PROJECTNAME)
