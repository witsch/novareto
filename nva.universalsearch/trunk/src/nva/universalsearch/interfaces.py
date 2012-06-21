from zope.interface import Interface
from zope.schema import TextLine, List
from collective.indexing.interfaces import IIndexQueueProcessor
from nva.universalsearch import MessageFactory as _


class IUniversalSearchQueueProcessor(IIndexQueueProcessor):
    pass


class IUniversalSearchSchema(Interface):

    systems = List(title=_(u'Available sites'),
        description=_(u'Plone sites to be included in search results.'),
        value_type=TextLine(), default=[], required=False)


class IUniversalSearchConfig(IUniversalSearchSchema):
    """ utility to hold configuration values regarding universal search """
