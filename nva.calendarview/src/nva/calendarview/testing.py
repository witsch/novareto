from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class NvaCalendarview(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import nva.calendarview
        xmlconfig.file('configure.zcml',
                       nva.calendarview,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nva.calendarview:default')

NVA_CALENDARVIEW_FIXTURE = NvaCalendarview()
NVA_CALENDARVIEW_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NVA_CALENDARVIEW_FIXTURE, ),
                       name="NvaCalendarview:Integration")