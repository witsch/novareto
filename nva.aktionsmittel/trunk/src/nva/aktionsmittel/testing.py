from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class NvaAktionsmittel(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import nva.aktionsmittel
        xmlconfig.file('configure.zcml',
                       nva.aktionsmittel,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nva.aktionsmittel:default')

NVA_AKTIONSMITTEL_FIXTURE = NvaAktionsmittel()
NVA_AKTIONSMITTEL_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NVA_AKTIONSMITTEL_FIXTURE, ),
                       name="NvaAktionsmittel:Integration")