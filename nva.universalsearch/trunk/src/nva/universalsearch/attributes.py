from zope.interface import Interface
from zope.component import getMultiAdapter
from plone.indexer import indexer


@indexer(Interface)
def system(obj, **kwargs):
    """ return title of plone site """
    system = getMultiAdapter((obj, obj.REQUEST), name="plone_portal_state")
    return system.portal_title()


@indexer(Interface)
def uri(obj, **kwargs):
    """ return absolute url """
    return obj.absolute_url()
