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
from uvclight.backends.zodb import Root
from cromlech.zodb import get_size, Site
from cromlech.zodb import initialize_applications

view_lookup = ViewLookup(view_locator(query_view))


class Root(Root):
    implements(IPublicationRoot)

    title = u"Example Site"
    description = u"An Example application."

KEY = "zodb.connection"

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
            conn = request.environment[KEY]
            site = get_site(conn, self.name)
            with Site(site) as site:
                response = publisher.publish(request, site, handle_errors=True)
            return response(environ, start_response)
        return publish(environ, start_response)

def create_db(db):
    initialize_applications(db, lambda: {'chemiedp' : Root})
