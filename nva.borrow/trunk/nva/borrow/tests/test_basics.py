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
        new_id = self.portal.invokeFactory('nva.borrow.borrowableitems', id='aktionsmittel-set', title='Aktionsmittelset')
        self.assertEqual(self.portal[new_id].portal_type, 'nva.borrow.borrowableitems')

    def testCreateItem(self):
        self.login('god')
        new_id = self.portal.invokeFactory('nva.borrow.borrowableitem', id='aktionsmittel', title='Aktionsmittel')
        self.assertEqual(self.portal[new_id].portal_type, 'nva.borrow.borrowableitem')

def test_suite():
    from unittest2 import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(BasicTests))
    return suite
