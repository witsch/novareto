# -*- coding: utf-8 -*-


from cromlech.browser import IPublicationRoot
from zope.interface import implements
from zope.location import Location
from zope.component import getGlobalSiteManager
from uvclight.utils import Site
from uvclight.bricks import Publication  # SecurePublication
from uvclight.backends.zodb import Root, ZODBPublication
from uvclight.utils import with_zcml, with_i18n


class MyRoot(Root):
    pass


class Application(ZODBPublication):

    @classmethod
    @with_zcml('zcml_file')
    @with_i18n('langs', fallback='en')
    def create(cls, gc, **kwargs):
        return super(Application, cls).create(root=MyRoot, **kwargs)
