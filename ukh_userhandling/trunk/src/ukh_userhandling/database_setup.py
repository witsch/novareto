# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok


from z3c.saconfig import EngineFactory, GloballyScopedSession
from sqlalchemy import Table, MetaData, create_engine
from z3c.saconfig.interfaces import IEngineCreatedEvent

DSN = 'ibm_db_sa://smartimp:smart09ukh@10.64.2.1:446/S65D4DBA'

engine_factory = EngineFactory(DSN, echo=False)
scoped_session = GloballyScopedSession()

grok.global_utility(engine_factory, direct=True)
grok.global_utility(scoped_session, direct=True)


engine = engine_factory()
metadata = MetaData(bind=engine)

schema_name = "UKHINTERN"
schema_name2 = "ukhph"

users = Table('Z1EXT1AA', metadata, schema="UKHINTERN", autoload=True, autoload_with=engine)
mitik = Table('mitik', metadata, schema="ukhph", autoload=True, autoload_with=engine)
mitik2 = Table('mitik2', metadata, schema="ukhph", autoload=True, autoload_with=engine)

