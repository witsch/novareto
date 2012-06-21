from zope.component import adapts, queryUtility
from zope.formlib.form import FormFields
from zope.interface import implements
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm

from nva.universalsearch import MessageFactory as _
from nva.universalsearch.interfaces import IUniversalSearchSchema
from nva.universalsearch.interfaces import IUniversalSearchConfig


class ControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IUniversalSearchSchema)

    def getSystems(self):
        util = queryUtility(IUniversalSearchConfig)
        return getattr(util, 'systems', '')

    def setSystems(self, value):
        util = queryUtility(IUniversalSearchConfig)
        if util is not None:
            util.systems = value

    systems = property(getSystems, setSystems)


class ControlPanel(ControlPanelForm):

    form_fields = FormFields(IUniversalSearchSchema)

    label = _('Universal search settings')
    description = _('Settings regarding universal search.')
    form_name = _('Search settings')
