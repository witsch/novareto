# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok

from z3c.saconfig import Session
from zope.interface import Interface
from .database_setup import users


class CheckDatabaseConnectivity(grok.View):
    grok.context(Interface)
    grok.name('checkdb')
    grok.require('zope.Public')

    def render(self):
        session = Session()
        return str(session.query(users).count())

