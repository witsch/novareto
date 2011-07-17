# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


from zope.schema import *
from zope.interface import Interface


class IBenutzer(Interface):

    login = TextLine(
            title = u"Login",
            description = u"Bitte geben Sie den Login-Namen ein.",
            required = True,
            )

    name1 = TextLine(
            title = u"Name",
            description = u"Bitte geben Sie den Firmennamen ein.",
            required = True,
            )

    plz = TextLine(
            title = u"PLZ",
            description = u"Bitte geben Sie die Postleitzahl ein.",
            required = True,
            )
