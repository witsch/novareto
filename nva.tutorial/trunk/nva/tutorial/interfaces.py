# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from zope.schema import ValidationError
from tidylib import tidy_document

class HtmlValidationError(ValidationError):
    u"""Bei Deiner Eingabe handelt es sich nicht um gültigen HTML-Text. Bitte überprüfe\
            noch einmal ganz genau Dein Dokument."""

def validateHtml(value):
    from tidylib import tidy_document
    document, errors = tidy_document(value, options={'numeric-entities':1})
    print document
    print errors
    if errors:
        raise HtmlValidationError(value)
    return True

class ICheckHtml(Interface):
    """Felder des Testformulars"""

    htmltext = schema.Text(title=u"HTML-Text",
            description=u"Bitte schreibe Dein HTML-Dokument in dieses Feld um zu testen ob es wie gewünscht\
                         funktioniert. Bitte beachte aber, dass wir Deinen Text nicht speichern können.\
                         Idealerweise nutzt Du also dieses Werkzeug nur für ganz kleine Schnipsel HTML-Code.",
            )
