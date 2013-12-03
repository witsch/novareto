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

from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.component import getUtility
from zope.interface import alsoProvides

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

# Interface class; used to define content-type schema.

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

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class TwitterProfile(Container):
    grok.implements(ITwitterProfile)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# twitter_profile_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ITwitterProfile)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
