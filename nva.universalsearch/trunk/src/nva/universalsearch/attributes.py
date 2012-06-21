from zope.interface import Interface
from zope.component import getMultiAdapter, getUtility
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName
from nva.universalsearch.interfaces import IUniversalSearchConfig


@indexer(Interface)
def system(obj, **kwargs):
    """ return title of plone site """
    system = getMultiAdapter((obj, obj.REQUEST), name="plone_portal_state")
    return system.portal_title()


@indexer(Interface)
def uri(obj, **kwargs):
    """ return absolute url """
    site_url = getUtility(IUniversalSearchConfig).site_url
    if site_url is None:
        return obj.absolute_url()
    else:
        url = getToolByName(obj, 'portal_url').getRelativeContentURL(obj)
        return site_url.rstrip('/') + '/' + url
