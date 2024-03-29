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
        searchable = 1,
        widget=atapi.RichWidget(
            label=_(u"Text"),
            description=_(u"Field description"),
        ),
    ),

    atapi.TextField(
        'beschreibung',
        storage=atapi.AnnotationStorage(),
        default_output_type = 'text/x-html-safe',
        searchable = 1,
        widget=atapi.RichWidget(
            label=_(u"Beschreibung"),
            description=_(u"Beschreibung description"),
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
        max_size=(150,216),
        widget=atapi.ImageWidget(
            label=_(u"Bild"),
            macro="custom_image",
            description=_(u"Bild des Artikels."),
        ),
        sizes = {'large'   : (768, 768),
                 'preview' : (400, 400),
                 'mini'    : (200, 200),
                 'thumb'   : (128, 128),
                },
        #validators=('isNonEmptyFile'),
    ),

  atapi.TextField(
        'tax',
        storage=atapi.AnnotationStorage(),
        default = '1',
        vocabulary=(
              ('1', 'Preisangaben verstehen sich zzgl. gesetzl. MwSt. und Versandkosten.'),
              ('2', 'Preisangaben verstehen sich zzgl. gesetzl. Mwst. .')), 
        widget=atapi.SelectionWidget(
            label=_(u"Mwst Informationen"),
        ),
    ),

    atapi.FixedPointField(
        'preis',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Preis fuer Mitglieder"),
            description=_(u"Bitte geben Sie hier den Preis an, der fuer Mitglieder gilt."),
        ),
        validators=('isDecimal'),
    ),

    atapi.BooleanField(
        'preisinfo',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"Preis Information / Member"),
            description=_(u"Mitglieder erhalten 3 Exemplare kostenlos."),
        ),
    ),

    atapi.FixedPointField(
        'preis_non_member',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Preis fuer Nicht-Mitglieder"),
            description=_(u"Bitte geben Sie hier den Preis an, der fuer Nicht-Mitglieder gilt."),
        ),
        validators=('isDecimal'),
    ),

   atapi.FileField(
        'file',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Broschuere"),
            macro="custom_file",
            description=_(u"Bitte hier die Broschure uploaden."),
        ),
        validators=('isNonEmptyFile'),
    ),

   atapi.IntegerField(
        'quantity',
        default = 99,
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(
            label=_(u"Maximum quantity"),
        ),
    ),

    atapi.StringField(
        'status',
        storage=atapi.AnnotationStorage(),
        default = 'lieferbar',
        vocabulary =  ( 'lieferbar',
                        'nicht lieferbar' ),
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
    preis_non_member = atapi.ATFieldProperty('preis_non_member')
    preisinfo = atapi.ATFieldProperty('preisinfo')
    quantity = atapi.ATFieldProperty('quantity')
    status = atapi.ATFieldProperty('status')
    tax = atapi.ATFieldProperty('tax')
    text = atapi.ATFieldProperty('text')
    beschreibung = atapi.ATFieldProperty('beschreibung')
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


    def validate_quantity(self, value):
        if not value.isdigit():
            return _(u"Bitte nur ganze Zahlen eingeben")
        if int(value) <= 0 or int(value) >= 100:
            return _(u"Bitte nur Werte zwischen 1 und 99 eintragen")


atapi.registerType(Artikel, PROJECTNAME)

from nva.cart import IDiscountedCartItem
from zope.interface import directlyProvides

class BuyableContentAdapter(CartItem, grok.Adapter):
    """A cart item adapter
    """
    grok.context(IArtikel)
   
    def __init__(self, context):
        print "ININ"
        self.title = unicode(context.Title(), 'utf-8')
        self.url = context.absolute_url()
        self.code = context.code
        self.price = float(context.preis)
        self.non_member_price = float(context.preis_non_member) 
        self.price_info = context.preisinfo
        self.max_quantity = context.quantity

    @property
    def discount_price(self):
        preis = self.price
        if self.price_info:
            preis = 0.0
            if self.quantity > 3:
                preis = self.price 
        return preis 

    @property
    def calculate_quantity(self):
        if self.price_info:
            if self.quantity > 3:
                return self.quantity - 3 
        return self.quantity
        
    def total_price(self, member=True):
        #if not IDiscountedCartItem.providedBy(self) or not member:
        if not member:
            return self.discount_price * self.calculate_quantity
        return self.non_member_price * self.quantity

    def basic_price(self, member=True):
        #if not IDiscountedCartItem.providedBy(self):
        if not member:
            return self.discount_price 
        return self.non_member_price

    @property
    def portlet_member_price(self):
        return self.discount_price * self.calculate_quantity

    @property
    def portlet_total_price(self):
        return self.non_member_price * self.quantity
