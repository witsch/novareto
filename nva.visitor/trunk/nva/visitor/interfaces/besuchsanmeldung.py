from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from nva.visitor import visitorMessageFactory as _



class IBesuchsanmeldung(Interface):
    """Spezielle Form eines Termins zur Anmeldung von Besuchern im Intranet."""

    # -*- schema definition goes here -*-
    mailsent = schema.Bool(
        title=_(u"Mailinformation"),
        required=False,
        description=_(u"Ueber die Besuchsanmeldung wurde per Mail informiert."),
    )
#
    firma = schema.TextLine(
        title=_(u"Firma"),
        required=True,
        description=_(u"Firmenname des Besuchers"),
    )
#
    ortland = schema.TextLine(
        title=_(u"Ort/Land"),
        required=True,
        description=_(u"Herkunft des Besuchers (Ort/Land)"),
    )
#
    brancheaktivitaeten = schema.List(
        title=_(u"Branche"),
        required=True,
        description=_(u"Auswahl der Branche / Aktivitaeten des Besuchers"),
    )
#
    gbeziehung = schema.List(
        title=_(u"Geschaeftsbeziehung"),
        required=True,
        description=_(u"Auswahl der Art der Geschaeftsbeziehung"),
    )
#
    ansprechpartner = schema.TextLine(
        title=_(u"Ansprechpartner"),
        required=True,
        description=_(u"Name des Besuchers / Ansprechpartners"),
    )
#
    funktion = schema.TextLine(
        title=_(u"Funktion"),
        required=True,
        description=_(u"Funktion des Besuchers / Ansprechpartners"),
    )
#
    enddate = schema.Date(
        title=_(u"Besuchsende (Termin)"),
        required=False,
        description=_(u"Tragen Sie das vereinbarte Besuchsende ein oder klicken Sie auf das Kalender-Icon und treffen eine Auswahl."),
    )
#
    startdate = schema.Date(
        title=_(u"Besuchsbeginn (Termin)"),
        required=True,
        description=_(u"Tragen Sie den vereinbarten Bessuchsbeginn ein oder klicken Sie auf das Kalender-Icon und treffen eine Auswahl."),
    )
#
    ablauf = schema.Text(
        title=_(u"zeitlicher Ablauf des Besuches"),
        required=False,
        description=_(u"Kurze Darstellung des zeitlichen Ablaufs."),
    )
#
    mylocation = schema.TextLine(
        title=_(u"Ort"),
        required=True,
        description=_(u"Ort des Besuches"),
    )
#
    grund = schema.TextLine(
        title=_(u"Grund"),
        required=True,
        description=_(u"Grund des Besuches"),
    )
#
    themen = schema.Text(
        title=_(u"Themen"),
        required=True,
        description=_(u"Kurze Darstellung der Gespraechsthemen"),
    )
#
    contactname = schema.TextLine(
        title=_(u"Kontaktperson"),
        required=False,
        description=_(u"Kontaktperson bei Pfister"),
    )
#
    contactphone = schema.TextLine(
        title=_(u"Kontakt Telefon"),
        required=False,
        description=_(u"Tragen Sie hier eine Telefonnummer ein, unter der man weitere Informationen anfordern oder buchen kann."),
    )
#
    gespraechsteilnehmer = schema.Text(
        title=_(u"Teilnehmer am Gespraech"),
        required=True,
        description=_(u"Namen der Gespraechsteilnehmer"),
    )
#
    mailing = schema.TextLine(
        title=_(u"zusaetzlich per E-Mail informieren"),
        required=False,
        description=_(u"Hier koennen Empfaenger ausgewaehlt werden, die per E-Mail ueber den Termin benachrichtigt werden sollen. Mitglieder der Geschaeftsfuehrung und die Pforte werden immer informiert."),
    )
#
