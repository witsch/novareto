# -*- coding: utf-8 -*-
# Copyright (c) 2007-2014 NovaReto GmbH
# cklinger@novareto.de

import pytest
import chemiedp
import chemiedp.utils

from paste.deploy import loadapp
from uvclight.tests.testing import configure


@pytest.fixture(scope="session")
def config(request):
    """loading the zca with configure.zcml of this package"""
    return configure(request, chemiedp, 'configure.zcml')


@pytest.fixture(scope="session")
def app(request):
    """ load the paste.deploy wsgi environment from deploy.ini"""
    deploy_ini = "config:/Users/christian/work/ab_backend/cdp/parts/etc/test.ini"
    return loadapp(deploy_ini, name="main", global_conf={})


@pytest.fixture(scope="session")
def root(request):
    """ create an instance of the application"""
    return chemiedp.utils.MyRoot()
