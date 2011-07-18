# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


from zope.schema import *
from zope.interface import Interface


class IBenutzer(Interface):

    name1 = TextLine(
            title = u"Name",
            description = u"Bitte geben Sie den Firmennamen ein.",
            required = False,
            )

    plz = TextLine(
            title = u"PLZ",
            description = u"Bitte geben Sie die Postleitzahl ein.",
            required = False,
            )

    ort = TextLine(
            title = u"Ort",
            description = u"Bitte geben Sie den Ort des Unternehmens ein.",
            required = False,
            )



class IChangePassword(Interface):

    passwort = TextLine(
            title = u"Passwort",
            description = u"Bitte geben Sie das neue Passwort ein."
            )

    best_pw = TextLine(
            title = u"Bestätigung",
            description = u"Bitte wiederholen Sie das Passwort hier."
            )
