from five import grok
from datetime import datetime
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from nva.socialroom import MessageFactory as _

from plone.app.portlets.portlets.rss import RSSFeed

FEED_DATA = {}

class IRSSReader(form.Schema, IImageScaleTraversable):
    """
    A Reader for a Special RSS-Feed.
    """

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    url = schema.TextLine(title=_(u'URL of RSS feed'),
                        description=_(u'Link of the RSS feed to display.'),
                        required=True,
                        default=u'')

    timeout = schema.Int(title=_(u'Feed reload timeout'),
                        description=_(u'Time in minutes after which the feed should be reloaded.'),
                        required=True,
                        default=100)

class RSSReader(Container):
    grok.implements(IRSSReader)

    def getFeed(self):
        """return a feed object but do not update it"""
        feed = FEED_DATA.get(self.url, None)
        if feed is None:
            # create it
            feed = FEED_DATA[self.url] = RSSFeed(self.url, self.timeout)
        return feed

    def getSocialContent(self):
        feed = self.getFeed()
        feed.update()
        results = feed.items[:self.count]
        sc = []
        for i in results:
            entry = {}
            entry['title'] = i.get('title')
            desctxt = i.get('summary')
            if len(desctxt) > 160:
                desctxt = desctxt[:160]
                cutter = desctxt.rfind(' ')
                desctxt = desctxt[:cutter] + '...'
            entry['description'] = desctxt
            entry['url'] = i.get('url')
            entry['date'] = i.get('updated').strftime('%d.%m.%Y %H:%M')
            entry['thumb'] = ''
            sc.append(entry)
        return sc

class RSSView(grok.View):
    """ sample view class """

    grok.context(IRSSReader)
    grok.require('zope2.View')

    @property
    def initializing(self):
        """should return True if deferred template should be displayed"""
        feed=self._getFeed()
        if not feed.loaded:
            return True
        if feed.needs_update:
            return True
        return False

    def deferred_update(self):
        """refresh data for serving via KSS"""
        feed = self._getFeed()
        feed.update()

    def update(self):
        """update data before rendering. We can not wait for KSS since users
        may not be using KSS."""
        self.deferred_update()

    def _getFeed(self):
        return self.context.getFeed()

    @property
    def url(self):
        """return url of feed for portlet"""
        return self._getFeed().url

    @property
    def siteurl(self):
        """return url of site for portlet"""
        return self._getFeed().siteurl

    @property
    def feedlink(self):
        """return rss url of feed for portlet"""
        return self.context.url.replace("http://", "feed://")

    @property
    def title(self):
        """return title of feed for portlet"""
        return self._getFeed().title

    @property
    def feedAvailable(self):
        """checks if the feed data is available"""
        return self._getFeed().ok

    @property
    def items(self):
        return self._getFeed().items[:self.context.count]

    @property
    def enabled(self):
        return self._getFeed().ok
