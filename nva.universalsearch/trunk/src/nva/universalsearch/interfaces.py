from zope.interface import Interface
from zope.schema import TextLine, Choice, List
from collective.indexing.interfaces import IIndexQueueProcessor
from nva.universalsearch import MessageFactory as _


class IUniversalSearchQueueProcessor(IIndexQueueProcessor):
    pass


class IUniversalSearchSchema(Interface):

    site_url = TextLine(title=_(u'Site URL'),
        description=_(u'Canonical URL of the site.  Used for indexing URIs.'))

    systems = List(title=_(u'Available sites'),
        description=_(u'Plone sites to be included in search results.'),
        value_type=Choice(vocabulary='nva.universalsearch.systems'),
        default=[], required=False)


class IUniversalSearchConfig(IUniversalSearchSchema):
    """ utility to hold configuration values regarding universal search """
