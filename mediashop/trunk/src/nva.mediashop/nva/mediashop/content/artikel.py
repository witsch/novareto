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

    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'artikel_nr',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Artikel Nummer"),
            description=_(u"Field description"),
        ),
    ),

    atapi.FixedPointField(
        'preis',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Preis"),
            description=_(u"Field description"),
        ),
        validators=('isDecimal'),
    ),

    atapi.StringField(
        'stand',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"New Field"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'status',
        storage=atapi.AnnotationStorage(),
        vocabulary = ['Bestellen', 
                      'Dieser Artikel ist derzeit leider vergriffen'],
        widget=atapi.SelectionWidget(
            label=_(u"New Field"),
            description=_(u"Field description"),
        ),
    ),


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
    status = atapi.ATFieldProperty('status')

    preis = atapi.ATFieldProperty('preis')

    stand = atapi.ATFieldProperty('stand')

    text = atapi.ATFieldProperty('text')

    artikel_nr = atapi.ATFieldProperty('artikel_nr')


atapi.registerType(Artikel, PROJECTNAME)




class BuyableContentAdapter(object):

    implements(IBuyableContent)

    def __init__(self, context):
        self.context = context
        self.price = float(self.context.preis) 
        self.product_code = self.context.artikel_nr 
        self.weight = 0 

