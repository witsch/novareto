"""Definition of the Artikel content type
"""

import five.grok as grok
from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from nva.cart import CartItem, ICartAddable, IDiscountedCartItem
from nva.mediashop import mediashopMessageFactory as _
from nva.mediashop.interfaces import IArtikel
from nva.mediashop.config import PROJECTNAME

ArtikelSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        default_output_type = 'text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'code',
        required=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Artikel Nummer"),
            description=_(u"Field description"),
        ),
    ),

    atapi.StringField(
        'stand',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Stand"),
        ),
    ),

   atapi.ImageField(
        'image',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Bild"),
            description=_(u"Bild des Artikels."),
        ),
        sizes = {'large'   : (768, 768),
                 'preview' : (400, 400),
                 'mini'    : (200, 200),
                 'thumb'   : (128, 128),
                },
        validators=('isNonEmptyFile'),
    ),

  atapi.TextField(
        'tax',
        storage=atapi.AnnotationStorage(),
        vocabulary=(
              ('1', 'Preisangaben verstehen sich zzgl. MwSt. und Versandkosten'),
              ('2', 'Preisangaben verstehen sich zzgl. Mwst.')), 
        widget=atapi.SelectionWidget(
            label=_(u"Mwst Informationen"),
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
        'preisinfo',
        storage=atapi.AnnotationStorage(),
        vocabulary= (
                ('1', 'Preis ist gleich für Mitglieder und nicht Mitglieder.'),
                ('2', 'Mitglieder erhalten den Artikel unentgeltlich.'),
                ('3', 'Mitglieder erhalten einen Rabatt von 50% des Artikelpreises.'),
                ('4', 'Mitglieder zahlen ab einer Menge von mehr als 4 Stck. den vollen Artikelpreis.')),
        widget=atapi.SelectionWidget(
            label=_(u"Preis Information / Member"),
            description=_(u"Field description"),
        ),
    ),

   atapi.FileField(
        'file',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Broschuere"),
            description=_(u"Bitte hier die Broschure uploaden."),
        ),
        validators=('isNonEmptyFile'),
    ),

   atapi.IntegerField(
        'quantity',
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(
            label=_(u"Maximum quantity"),
        ),
    ),

    atapi.StringField(
        'status',
        storage=atapi.AnnotationStorage(),
        vocabulary =  ( 'lieferbar',
                        'vergriffen' ),
        widget=atapi.SelectionWidget(
            label=_(u"Status"),
            description=_(u"Ist dieser Artikel momentan Lieferbar?"),
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
    implements(IArtikel, ICartAddable)

    meta_type = "Artikel"
    schema = ArtikelSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    code = atapi.ATFieldProperty('code')
    file = atapi.ATFieldProperty('file')
    image = atapi.ATFieldProperty('image')
    preis = atapi.ATFieldProperty('preis')
    preisinfo = atapi.ATFieldProperty('preisinfo')
    quantity = atapi.ATFieldProperty('quantity')
    status = atapi.ATFieldProperty('status')
    tax = atapi.ATFieldProperty('tax')
    text = atapi.ATFieldProperty('text')
    stand = atapi.ATFieldProperty('stand')

    # workaround to make resized images
    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return base.ATCTContent.__bobo_traverse__(self, REQUEST, name)


atapi.registerType(Artikel, PROJECTNAME)


class BuyableContentAdapter(CartItem, grok.Adapter):
    """A cart item adapter
    """
    grok.context(IArtikel)
   
    def __init__(self, context):
        self.title = unicode(context.Title(), 'utf-8')
        self.url = context.absolute_url()
        self.code = context.code
        self.price = float(context.preis) 
        self.price_info = context.preisinfo
        self.max_quantity = context.quantity

    @property
    def discount_price(self):
        if self.price_info == '1':
            preis = self.price
        elif self.price_info == '2':
            preis = 0
        elif self.price_info == '3':
            preis = self.price / 2
        elif self.price_info == '4':
            preis = 0
            if self.quantity > 4:
                preis = self.price 
        return preis 

    @property
    def calculate_quantity(self):
        if self.price_info == '4':
            if self.quantity > 4:
                return self.quantity - 4
        return self.quantity
        
    @property
    def total_price(self):
        if not IDiscountedCartItem.providedBy(self):
            return self.discount_price * self.calculate_quantity
        return self.price * self.quantity
    
