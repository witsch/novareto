# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import *

class IOrderForm(Interface):
    """ OrderForm"""

    mitgliedsnummer = TextLine(title=u"Mitgliedsnummer", required=False)
    name = TextLine(title=u"Name")
    vorname = TextLine(title=u"Vorname")
    firma = TextLine(title=u"Firma")
    strasse = TextLine(title=u"Straße")
    plz = TextLine(title=u"Postleitzahl")
    ort = TextLine(title=u"Ort")
    email = TextLine(title=u"E-Mail", required=True)
    telefon = TextLine(title=u"Telefon,", required=False)
    telefax = TextLine(title=u"Telefax", required=False)
    land = TextLine(title=u"Land", required=False)
    ustid = TextLine(title=u"USTID-Nr.", required=False)

    lieferadresse = Bool(title=u"Lieferadresse / Rechnungsadresse",
                         description=u"Wenn Sie eine abweichende Lieferadresse haben klicken Sie bitte hier.")
    lname = TextLine(title=u"Name", required=False)
    lstrasse = TextLine(title=u"Straße", required=False)
    lplz = TextLine(title=u"Postleitzahl", required=False)
    lort = TextLine(title=u"Ort", required=False)

    datenschutz = Bool(title=u"Datenschutzvereinbarung", 
                       description=u"Mit der Übermittlung meiner Adressdaten an das von der BG Verkehr"
                                    " beauftragte Versandunternehmen GSV GmbH erkläre ich mich einverstanden."
                                    " Die Adressdaten dienen ausschließlich dem einmaligen Versand. Eine"
                                    " Weitergabe der Daten an Dritte ist untersagt.",
                       required = True)

