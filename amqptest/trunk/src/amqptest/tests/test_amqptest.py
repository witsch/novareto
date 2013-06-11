import unittest

from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest

from zope.fanstatic.testing import ZopeFanstaticBrowserLayer

import amqptest.tests
from amqptest.app import Amqptest

# In this file we create a unittest, a functional unittest.

class MyTestCase(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(1, 1)

browser_layer = ZopeFanstaticBrowserLayer(amqptest.tests)

class MyFunctionalTestCase(unittest.TestCase):

    layer = browser_layer

    def test_foo(self):
        index = queryMultiAdapter((Amqptest(), TestRequest()), name='index')
        self.assertNotEqual(index, None)

        # There is no view called 'index2'
        index2 = queryMultiAdapter((Amqptest(), TestRequest()), name='index2')
        self.assertEqual(index2, None)

