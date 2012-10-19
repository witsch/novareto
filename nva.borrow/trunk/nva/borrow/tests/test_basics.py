################################################################
# nva.borrow
# (C) 2012, ZOPYX Ltd.
################################################################

import os
from base import TestBase

from zExceptions import Unauthorized

class BasicTests(TestBase):

    def testCreateContainer(self):
        self.login('god')
        new_id = self.portal.invokeFactory('nva.borrow.itemcontainer', id='aktionsmittel-set', title='Aktionsmittelset')
        self.assertEqual(self.portal[new_id].portal_type, 'nva.borrow.itemcontainer')

    def testCreateItem(self):
        self.login('god')
        new_id = self.portal.invokeFactory('nva.borrow.itemcontainer', id='aktionsmittel-set', title='Aktionsmittelset')
        container = self.portal[new_id]
        new_id = container.invokeFactory('nva.borrow.borrowableitem', id='aktionsmittel', title='Aktionsmittel')
        self.assertEqual(container[new_id].portal_type, 'nva.borrow.borrowableitem')

    def testSetupPFG(self):
        self.login('god')
        new_id = self.portal.invokeFactory('nva.borrow.itemcontainer', id='aktionsmittel-set', title='Aktionsmittelset')
        container = self.portal[new_id]
        container.restrictedTraverse('@@setupPFG')()

def test_suite():
    from unittest2 import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(BasicTests))
    return suite
