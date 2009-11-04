"""Definition of the Artikel content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from nva.mediashop import mediashopMessageFactory as _
from nva.mediashop.interfaces import IArtikel
from nva.mediashop.config import PROJECTNAME
from Products.PloneGetPaid.interfaces import IBuyableMarker, IShippableMarker
from getpaid.core.interfaces import IBuyableContent

ArtikelSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ArtikelSchema['title'].storage = atapi.AnnotationStorage()
ArtikelSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ArtikelSchema, moveDiscussion=False)

class Artikel(base.ATCTContent):
    """Artikel"""
    implements(IArtikel, 
               IBuyableMarker,
               )

    meta_type = "Artikel"
    schema = ArtikelSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Artikel, PROJECTNAME)




class BuyableContentAdapter(object):

    implements(IBuyableContent)

    def __init__(self, context):
        self.context = context
        self.price = 20.0 
        self.product_code = "3333"
        self.weight = 0 

