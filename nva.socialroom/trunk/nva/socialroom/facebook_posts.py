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
from facepy import GraphAPI

from nva.socialroom import MessageFactory as _


# Interface class; used to define content-type schema.

class IFacebookPosts(form.Schema, IImageScaleTraversable):
    """
    A content-Type to c collect the posts from a special account.
    """

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    facebook_user = schema.TextLine(title=_(u'Screen-Name of Facebook-User'),
                        description=_(u'Screen-Name of Facebook-User, you want to collect posts from.'),
                        required=True,
                        default=u'')

    oauth_token = schema.TextLine(title=_(u'Auth-Token to Login to facebook account'),
                        description=_(u'Enter here the OAuth Longlife Access Token.'),
                        required=True,
                        default=u'')


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class FacebookPosts(Container):
    grok.implements(IFacebookPosts)

    def getPosts(self):
        """get and format the posts from facebook-Account"""
        graph = GraphAPI(self.oauth_token)
        results = graph.get('%s/posts' %self.facebook_user)
        messages = results.get('data')[:self.count]
        fb_messages = []
        for i in messages:
            msg = {}
            if i.get('message'):
                msg['type'] = 'facebook'
                msg['description'] = i.get('message')
                msg['url'] = 'https://www.facebook.com/BGETEM'
                postdatetime = datetime.strptime(i.get('updated_time')[:19], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y %H:%M')
                msg['date'] = postdatetime
                if i.get('picture'):
                    msg['thumb'] = i.get('picture')
                else:
                    msg['thumb'] = ''
                fb_messages.append(msg)
        return fb_messages

    def getSocialContent(self):
        return self.getPosts()


# View class
# The view will automatically use a similarly named template in
# facebook_posts_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IFacebookPosts)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
