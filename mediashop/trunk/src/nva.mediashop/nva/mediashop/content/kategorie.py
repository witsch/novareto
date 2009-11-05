"""Definition of the Kategorie content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from nva.mediashop import mediashopMessageFactory as _
from nva.mediashop.interfaces import IKategorie
from nva.mediashop.config import PROJECTNAME

KategorieSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

KategorieSchema['title'].storage = atapi.AnnotationStorage()
KategorieSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    KategorieSchema,
    folderish=True,
    moveDiscussion=False
)

class Kategorie(folder.ATFolder):
    """Kategorie"""
    implements(IKategorie)

    meta_type = "Kategorie"
    schema = KategorieSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Kategorie, PROJECTNAME)
