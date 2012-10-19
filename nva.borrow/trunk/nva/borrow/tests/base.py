################################################################
# nva.borrow
# (C) 2012, ZOPYX Ltd.
################################################################

import os
import unittest2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import setRoles, login
from plone.testing import z2

from zope.configuration import xmlconfig
from AccessControl.SecurityManagement import newSecurityManager
from zope.component import getUtility

import nva.borrow
import Products.PloneFormGen
import collective.pfg.dexterity
import quintagroup.ploneformgen.readonlystringfield

os.environ['TESTING'] = '1'

class PolicyFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):

        for mod in (nva.borrow, 
                    Products.PloneFormGen, 
                    quintagroup.ploneformgen.readonlystringfield,
                    collective.pfg.dexterity): 
            xmlconfig.file('configure.zcml', mod, context=configurationContext)
        z2.installProduct(app, 'nva.borrow')
        z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'collective.pfg.dexterity')
        z2.installProduct(app, 'quintagroup.ploneformgen.readonlystringfield')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'nva.borrow:default')
        portal.acl_users.userFolderAddUser('god', 'dummy', ['Manager'], []) 
        setRoles(portal, 'god', ['Manager'])
        portal.acl_users.userFolderAddUser('ppr', 'dummy', ['PPR'], []) 
        setRoles(portal, 'ppr', ['Member', 'PPR'])
        portal.acl_users.userFolderAddUser('member', 'dummy', ['Member'], []) 
        setRoles(portal, 'member', ['Member'])
        login(portal, 'god')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'nva.borrow')


POLICY_FIXTURE = PolicyFixture()
POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(POLICY_FIXTURE,), name="PolicyFixture:Integration")

class TestBase(unittest2.TestCase):

    layer = POLICY_INTEGRATION_TESTING

    @property
    def portal(self):
        return self.layer['portal']

    def login(self, uid='god'):
        """ Login as manager """
        user = self.portal.acl_users.getUser(uid)
        newSecurityManager(None, user.__of__(self.portal.acl_users))

