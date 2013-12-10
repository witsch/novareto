from five import grok

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

from gdata.youtube.service import YouTubeService
from datetime import datetime

from nva.socialroom import MessageFactory as _


# Interface class; used to define content-type schema.

class IYouTubeFeed(form.Schema, IImageScaleTraversable):
    """
    A special feed from youtube.
    """

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    url = schema.TextLine(title=_(u'URL of Youtube feed'),
                        description=_(u'Link of the RSS feed to display.'),
                        required=True,
                        default=u'')

    timeout = schema.Int(title=_(u'Feed reload timeout'),
                        description=_(u'Time in minutes after which the feed should be reloaded.'),
                        required=True,
                        default=100)

    linkurl = schema.TextLine(title=_(u'Link-URL'),
                        description=_(u'URL to Link the object title.'),
                        required=False,
                        default=u'')

class YouTubeFeed(Container):
    grok.implements(IYouTubeFeed)

    def getFeed(self):
        """return a feed object from youtube channel"""
        yt_service = YouTubeService()
        FeedFormatted = self.FormatVideoFeed(yt_service.GetYouTubeVideoFeed(self.url))
        return FeedFormatted

    def FormatEntryDetails(self, feedentry):
        entry = {}
        entry['title'] = feedentry.media.title.text
        desctxt = feedentry.media.description.text
        if len(desctxt) > 160:
            desctxt = desctxt[:160]
            cutter = desctxt.rfind(' ')
            desctxt = desctxt[:cutter] + '...'
        entry['description'] = desctxt
        entry['url'] = feedentry.media.player.url
        entrydatetime = datetime.strptime(feedentry.published.text[:19], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')
        entry['date'] = entrydatetime
        thumbnails = feedentry.media.thumbnail
        if thumbnails:
            entry['thumb'] = thumbnails[0].url
        else:
            entry['thumb'] = ''
        return entry

    def FormatVideoFeed(self, feed):
        sc = []
        for entry in feed.entry[:self.count]:
            sc.append(self.FormatEntryDetails(entry))
        return sc

    def getSocialContent(self):
        return self.getFeed()

class SampleView(grok.View):
    """ sample view class """

    grok.context(IYouTubeFeed)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
