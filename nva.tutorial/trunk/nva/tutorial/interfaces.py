# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from zope.schema import ValidationError
#from tidylib import tidy_document

class HtmlValidationError(ValidationError):
    u"""Bei Deiner Eingabe handelt es sich nicht um gültigen HTML-Text. Bitte überprüfe\
            noch einmal ganz genau Dein Dokument."""

def validateHtml(value):
    from tidylib import tidy_document
    document, errors = tidy_document(value, options={'numeric-entities':1})
    if errors:
        raise HtmlValidationError(value)
    return True

class ICheckHtml(Interface):
    """Felder des Testformulars"""

    htmltext = schema.Text(title=u"HTML-Text",
            description=u"Bitte schreibe Deinen HTML-Code in dieses Feld um zu testen ob er wie gewünscht\
                         funktioniert. Bitte beachte aber, dass Dein Text hier nicht gespeichert bleibt.\
                         Du kannst Dir das Fenster in der rechten unteren Ecke so groß ziehen wie Du es brauchst.",
            )
