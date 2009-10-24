"""Definition of the ModeratorenContainer content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from nva.moderatorenliste import moderatorenlisteMessageFactory as _
from nva.moderatorenliste.interfaces import IModeratorenContainer
from nva.moderatorenliste.config import PROJECTNAME

ModeratorenContainerSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ModeratorenContainerSchema['title'].storage = atapi.AnnotationStorage()
ModeratorenContainerSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ModeratorenContainerSchema,
    folderish=True,
    moveDiscussion=False
)

class ModeratorenContainer(folder.ATFolder):
    """A Container for Moderator Items"""
    implements(IModeratorenContainer)

    meta_type = "ModeratorenContainer"
    schema = ModeratorenContainerSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ModeratorenContainer, PROJECTNAME)
