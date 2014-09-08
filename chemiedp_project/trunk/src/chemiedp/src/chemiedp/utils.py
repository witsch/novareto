# -*- coding: utf-8 -*-


from cromlech.configuration.utils import load_zcml
from cromlech.i18n import register_allowed_languages
from cromlech.dawnlight import DawnlightPublisher
from cromlech.browser import PublicationBeginsEvent, PublicationEndsEvent
from cromlech.browser import IPublicationRoot
from zope.interface import implements
from zope.location import Location
from zope.component.hooks import setSite
from zope.event import notify
from cromlech.webob.request import Request
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from zope.component import getGlobalSiteManager


view_lookup = ViewLookup(view_locator(query_view))


class Root(Location):
    implements(IPublicationRoot)

    title = u"Example Site"
    description = u"An Example application."

    def __init__(self, name):
        self.name = name

    def getSiteManager(self):
        return getGlobalSiteManager()


class Site(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        root = Root(self.name)
        setSite(root)
        return root

    def __exit__(self, exc_type, exc_value, traceback):
        setSite()


publisher = DawnlightPublisher(view_lookup=view_lookup)


class Application(object):

    def __init__(self, global_conf, name, zcml_file=None, session_key=None, langs='en'):
        load_zcml(zcml_file)
        allowed = langs.strip().replace(',', ' ').split()
        register_allowed_languages(allowed)
        self.name = name

    def __call__(self, environ, start_response):
        def publish(environ, start_response):
            request = Request(environ)
            with Site(self.name) as site:
                response = publisher.publish(request, site, handle_errors=True)
            return response(environ, start_response)
        return publish(environ, start_response)
