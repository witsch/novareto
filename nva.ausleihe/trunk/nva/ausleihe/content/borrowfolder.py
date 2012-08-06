"""Definition of the BorrowFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from nva.ausleihe.interfaces import IBorrowFolder
from nva.ausleihe.config import PROJECTNAME

BorrowFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BorrowFolderSchema['title'].storage = atapi.AnnotationStorage()
BorrowFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    BorrowFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class BorrowFolder(folder.ATFolder):
    """Folder for borrowable items"""
    implements(IBorrowFolder)

    meta_type = "BorrowFolder"
    schema = BorrowFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(BorrowFolder, PROJECTNAME)
