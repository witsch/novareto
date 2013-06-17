"""Definition of the Webcodeproxy content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from nva.webcodeproxy import webcodeproxyMessageFactory as _

from nva.webcodeproxy.interfaces import IWebcodeproxy
from nva.webcodeproxy.config import PROJECTNAME

WebcodeproxySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.LinesField(
        'extsystems',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Ids externer Systeme"),
            description=_(u"Hier koennen die mit den externen Systemen vereinbarten IDs eingetragen werden. Die Ids muessen mitgeliefert werden, um einen Webcode zu erhalten."),
        ),
        required=True,
    ),


    atapi.LinesField(
        'webcodes',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Webcodes"),
            description=_(u"Speicherung der Webcodes, die an externe Systeme ausgeliefert wurden."),
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

WebcodeproxySchema['title'].storage = atapi.AnnotationStorage()
WebcodeproxySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(WebcodeproxySchema, moveDiscussion=False)


class Webcodeproxy(base.ATCTContent):
    """Objekt zur Speicherung von Webcodes, die an externe Systeme ausgeliefert wurden."""
    implements(IWebcodeproxy)

    meta_type = "Webcodeproxy"
    schema = WebcodeproxySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    extsystems = atapi.ATFieldProperty('extsystems')

    webcodes = atapi.ATFieldProperty('webcodes')


atapi.registerType(Webcodeproxy, PROJECTNAME)
