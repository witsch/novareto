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
            required = False,)

    ort = schema.TextLine(
            title = u'Ort',
            description = u'Bitte geben Sie hier einen Ortsnamen ein falls Sie die Postleitzahl\
                    nicht zur Hand haben.',
            required = False,)

    name = schema.TextLine(
            title = u'Name',
            description = u'Bitte geben Sie hier den Nachnamen des Versicherten ein',
            required = True,)

