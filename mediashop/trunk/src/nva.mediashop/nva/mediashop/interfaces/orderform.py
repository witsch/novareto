from zope.interface import Interface
from zope.schema import *

class IOrderForm(Interface):
    """ OrderForm"""

    mitgliedsnummer = TextLine(title=u"Mitgliedsnummer", required=False)
    name = TextLine(title=u"Name")
    vorname = TextLine(title=u"Vorname")
    firma = TextLine(title=u"Firma")
    strasse = TextLine(title=u"Strasse")
    plz = TextLine(title=u"Postleitzahl")
    ort = TextLine(title=u"Ort")
    email = TextLine(title=u"Email", required=True)
    telefon = TextLine(title=u"Telefonnummer", required=False)
    telefax = TextLine(title=u"Telefax", required=False)
    land = TextLine(title=u"Land", required=False)
    ustid = TextLine(title=u"USTID-Nr", required=False)

    datenschutz = Bool(title=u"Datenschutzvereinbarung", 
                       description=u"Mit der Übermittlung meiner Daten an das",
                       required = True)

