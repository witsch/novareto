# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


from zope.schema import *
from zope.interface import Interface


class IBenutzer(Interface):

    mnr = TextLine(
            title = u"Mitgliedsnummer",
            description = u"Bitte geben Sie die Mitgliedsnummer ein.",
            required = False,
            )
    
    login = TextLine(
            title = u"Login",
            description = u"Bitte geben Sie den Anmeldenamen ein.",
            required = False,
            )
    
    
    name1 = TextLine(
            title = u"Name",
            description = u"Bitte geben Sie den Firmennamen ein.",
            required = False,
            )

    strasse = TextLine(
            title = u"Strasse",
            description = u"Bitte geben Sie die Strasse ein.",
            required = False,
            )

    ort = TextLine(
            title = u"Ort",
            description = u"Bitte geben Sie den Ort des Unternehmens ein.",
            required = False,
            )



class IChangePassword(Interface):

    oid = TextLine(
            title = u"OID",
            )

    login = TextLine(
            title = u"Anmeldename",
            )
    
    az = TextLine(
            title = u"Mitbenutzer",
            description = u"Aktenzeichen des Mitbenutzer. ('00' Bei Hauptbenutzer.)",
            )
    
    passwort = TextLine(
            title = u"Passwort",
            )
    
    email = TextLine(
            title = u"EMAIL",
            )

    vname = TextLine(
            title = u"Ansprechpartner Vorname"
            )
    
    nname = TextLine(
            title = u"Ansprechpartner Name"
            )
    
    vwhl = TextLine(
            title = u"Ansprechpartner Vorwahl"
            )
    
    tlnr = TextLine(
            title = u"Ansprechpartner Nummer"
            )
