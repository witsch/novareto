# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from uvc.validation import validatePLZ

class IUVCAnsprechpartnersuche(Interface):
    """Marker Interface"""

class IPlzOrtSuche(Interface):
    """Schema fuer die Suche nach Postleitzahl und Ort"""

    plz = schema.TextLine(
            title = u'PLZ',
            description = u'Bitte geben Sie hier die Postleitzahl ein.',
            required = True,)

    ort = schema.TextLine(
            title = u'Ort',
            description = u'Optional können Sie hier zusätzlich einen Ortsnamen angeben.',
            required = False,)

    name = schema.TextLine(
            title = u'Name',
            description = u'Bitte geben Sie hier den Nachnamen des Versicherten ein',
            required = True,)

