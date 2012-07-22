# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from Products.Archetypes.public import DisplayList

PROJECTNAME = 'nva.visitor'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Besuchsanmeldung': 'nva.visitor: Add Besuchsanmeldung',
}

branche = DisplayList((
    (u'Elektrotechnik', u'01 Elektrotechnik'),
    (u'Finanzdienstleister', u'02 Finanzdienstleister'),
    (u'FLS', u'03 FLS'),
    (u'Frachtführer', u'04 Frachtführer'),
    (u'Hardware/Software', u'05 Hardware/Software'),
    (u'Kraftwerk', u'06 Kraftwerk'),
    (u'Marketing', u'07 Marketing'),
    (u'Maschinenbau', u'08 Maschinenbau'),
    (u'Metallverarbeitung', u'09 Metallverarbeitung'),
    (u'Sekundärbrennstoffe', u'10 Sekundärbrennstoffe'),
    (u'sonstige Dienstleister', u'11 sonstige Dienstleister'),
    (u'sonstige Schwestergesellschaften', u'12 sonstige Schwestergesellschaften'),
    (u'Waren und Dienstleistungen am Bau', u'13 Waren und Dienstleistungen am Bau'),
    (u'Zement', u'14 Zement'),
    ))

beziehung = DisplayList((
    (u'Kunde', u'Kunde'),
    (u'Lieferant', u'Lieferant'),
    (u'Sonstige',u'Sonstige'),
    ))

