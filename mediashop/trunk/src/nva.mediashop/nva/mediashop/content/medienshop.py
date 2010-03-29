"""Definition of the MedienShop content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from nva.mediashop import mediashopMessageFactory as _
from nva.mediashop.interfaces import IMedienShop
from nva.mediashop.config import PROJECTNAME

MedienShopSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        default_output_type = 'text/x-html-safe',
        searchable = 1,
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Field description"),
        ),
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MedienShopSchema['title'].storage = atapi.AnnotationStorage()
MedienShopSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    MedienShopSchema,
    folderish=True,
    moveDiscussion=False
)

class MedienShop(folder.ATFolder):
    """MedienShop"""
    implements(IMedienShop)

    meta_type = "MedienShop"
    schema = MedienShopSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(MedienShop, PROJECTNAME)
