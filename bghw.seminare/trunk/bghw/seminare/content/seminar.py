"""Definition of the Seminar content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from bghw.seminare.interfaces import ISeminar
from bghw.seminare.config import PROJECTNAME

SeminarSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SeminarSchema['title'].storage = atapi.AnnotationStorage()
SeminarSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SeminarSchema, moveDiscussion=False)


class Seminar(base.ATCTContent):
    """Beschreibung der Eigenschaften des SSeminars"""
    implements(ISeminar)

    meta_type = "Seminar"
    schema = SeminarSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Seminar, PROJECTNAME)
