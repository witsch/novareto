from plone.app.content.item import Item
from nva.mediashop.utils import setDefaultFields
from nva.mediashop.interfaces import IOrderForm
from zope.component import getMultiAdapter
from zope.interface import implements


class ShippingInformation(Item):
    """Persistent shipping informations.
    """
    implements(IOrderForm)
    meta_type = portal_type = 'ShippingInformation'
    Title = getTitle = lambda self:u"Shipping information"


# We set the default fields on the class itself.
setDefaultFields(ShippingInformation, [IOrderForm,])
