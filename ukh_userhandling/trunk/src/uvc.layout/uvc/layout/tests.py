import os.path
import z3c.testsetup
import uvc.layout
from zope.app.testing.functional import ZCMLLayer


ftesting_zcml = os.path.join(
    os.path.dirname(uvc.layout.__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer',
                            allow_teardown=True)

globs = {'__name__': 'uvc.layout'}

test_suite = z3c.testsetup.register_all_tests('uvc.layout', globs=globs)
