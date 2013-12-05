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

from datetime import datetime
from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.component import getUtility
from zope.interface import alsoProvides
from collective.prettydate.interfaces import IPrettyDate
import twitter
import logging

logger = logging.getLogger('nva.socialroom')

from nva.socialroom import MessageFactory as _

def TwitterAccounts(context):
    registry = getUtility(IRegistry)
    accounts = registry['collective.twitter.accounts']
    if accounts:
        vocab = accounts.keys()
    else:
        vocab = []
    return SimpleVocabulary.fromValues(vocab)

alsoProvides(TwitterAccounts, IContextSourceBinder)

def cache_key_simple(func, var):
    #let's memoize for 10 minutes or if any value of the portlet is modified
    timeout = time() // (60 * 10)
    return (timeout,
            var.data.tw_account,
            var.data.tw_user,
            var.data.max_results)

class ITwitterProfile(form.Schema, IImageScaleTraversable):
    """
    Read content from twitter account.
    """

    tw_account = schema.Choice(title=_(u'Twitter account'),
                               description=_(u"Which twitter account to use."),
                               required=True,
                               source=TwitterAccounts)

    tw_user = schema.TextLine(title=_(u'Twitter user'),
                              description=_(u"The Twitter user you wish to get feed from (you can include or omit the initial @)."),
                              required=True)

    max_results = schema.Int(title=_(u'Maximum results'),
                               description=_(u"The maximum results number."),
                               required=True,
                               default=5)

    pretty_date = schema.Bool(title=_(u'Pretty dates'),
                              description=_(u"Show dates in a pretty format (ie. '4 hours ago')."),
                              default=True,
                              required=False)

class TwitterProfile(Container):
    grok.implements(ITwitterProfile)

    def getAllTweets(self):
        registry = getUtility(IRegistry)
        accounts = registry.get('collective.twitter.accounts')
        account = accounts.get(self.tw_account)
        tw = twitter.Api(consumer_key=account.get('consumer_key'),
                         consumer_secret=account.get('consumer_secret'),
                         access_token_key=account.get('oauth_token'),
                         access_token_secret=account.get('oauth_token_secret'),)
        tw_user = self.tw_user
        max_results = self.max_results

        try:
            results = tw.GetUserTimeline(tw_user, count=max_results)
            logger.info("%s results obtained." % len(results))
        except Exception, e:
            logger.info("Something went wrong: %s." % e)
            results = []
        return results

    def getTweet(self, result):
        URL_TEMPLATE = """ 
        <a href="%s" target="blank_">%s</a>
        """
        HASHTAG_TEMPLATE = """ 
        <a href="http://twitter.com/#!/search?q=%s" target="blank_">%s</a>
        """
        USER_TEMPLATE = """ 
        <a href="http://twitter.com/#!/%s" target="blank_">%s</a>
        """
        full_text = result.GetText()
        split_text = full_text.split(' ')

        for index, word in enumerate(split_text):
            if word.startswith('@'):
                split_text[index] = USER_TEMPLATE % (word[1:], word)
            elif word.startswith('#'):
                split_text[index] = HASHTAG_TEMPLATE % ("%23" + word[1:], word)
            elif word.startswith('http'):
                split_text[index] = URL_TEMPLATE % (word, word)

        return "<p>%s</p>" % ' '.join(split_text)

    def getTweetUrl(self, result):
        return "https://twitter.com/%s/status/%s" % \
            (result.user.screen_name, result.id)

    def getReplyTweetUrl(self, result):
        return "https://twitter.com/intent/tweet?in_reply_to=%s" % result.id

    def getReTweetUrl(self, result):
        return "https://twitter.com/intent/retweet?tweet_id=%s" % result.id

    def getFavTweetUrl(self, result):
        return "https://twitter.com/intent/favorite?tweet_id=%s" % result.id

    def getDate(self, result):
        if self.pretty_date:
            date_utility = getUtility(IPrettyDate)
            date = date_utility.date(result.GetCreatedAt())
        else:
            date = DateTime.DateTime(result.GetCreatedAt())

        return date

    def getSocialContent(self):
        results = self.getAllTweets()
        sc = []
        for i in results:
            entry = {}
            entry['title'] = i.GetText()
            entry['description'] = ''
            entry['url'] = self.getTweetUrl(i)
            datum = i.GetCreatedAt().split(' ')
            formdatum = '%s %s %s %s' %(datum[2], datum[1], datum[5], datum[3])
	    try:
                entry['date'] = datetime.strptime(formdatum, '%d %b %Y %H:%M:%S').strftime('%d.%m.%Y %H:%M')
            except:
	        entry['date'] = formdatum
            sc.append(entry)
        return sc

class TwitterView(grok.View):
    """ sample view class """

    grok.context(ITwitterProfile)
    grok.require('zope2.View')

    def update(self):
        self.results = self.context.getAllTweets()
        self.pretty_date = self.context.pretty_date

    def getTweet(self, result):
        return self.context.getTweet(result)

    def getTweetUrl(self, result):
        return self.context.getTweetUrl(result)

    def getReplyTweetUrl(self, result):
        return self.context.getReplyTweetUrl(result)

    def getReTweetUrl(self, result):
        return self.context.getReTweetUrl(result)

    def getFavTweetUrl(self, result):
        return self.context.getFavTweetUrl(result)

    def getDate(self, result):
        return self.context.getDate(result)
