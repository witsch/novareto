# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok


from z3c.saconfig import EngineFactory, GloballyScopedSession
from sqlalchemy import Table, MetaData, create_engine
from z3c.saconfig.interfaces import IEngineCreatedEvent
from zope.app.appsetup.product import getProductConfiguration

config = getProductConfiguration('database')
DSN = config['dsn']


engine_factory = EngineFactory(DSN, echo=False)
scoped_session = GloballyScopedSession()

grok.global_utility(engine_factory, direct=True)
grok.global_utility(scoped_session, direct=True)


engine = engine_factory()
metadata = MetaData(bind=engine)

users = Table(config['users'], metadata, schema="UKHINTERN", autoload=True, autoload_with=engine)
z1ext1ab = Table(config['z1ext1ab'], metadata, schema="UKHINTERN", autoload=True, autoload_with=engine)
