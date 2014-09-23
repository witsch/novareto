# -*- coding: utf-8 -*-


from cromlech.browser import IPublicationRoot
from zope.interface import implements
from zope.location import Location
from zope.component import getGlobalSiteManager
from uvclight.utils import Site
from uvclight.bricks import Publication  # SecurePublication
from uvclight.backends.zodb import Root, ZODBPublication


class Application(ZODBPublication):

    def site_manager(self, environ):
        return Site(Root, self.name)
