from zope.interface import Interface, implements
from zope import schema
from nva.userdata import _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

def validateAccept(value):
    if not value == True:
        return False
    return True

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema

class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    telefon = schema.TextLine(
        title=_(u'Telefonnumer'),
        description=_(u'Bitte tragen Sie hier die Festnetznummer ein.'),
        required=False,
        )
    mobile = schema.TextLine(
        title=_(u'Mobilrufnummer'),
        description=_(u'Bitte tragen Sie hier (wenn vorhanden) die Mobilrufnummer ein.'),
        required=False,
        )

