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


from nva.socialroom import MessageFactory as _


# Interface class; used to define content-type schema.

class ISocialNewsroom(form.Schema, IImageScaleTraversable):
    """
    A Folder to accumulate content from social networks.
    """

    details = RichText(
            title = _(u'Beschreibung der Details zum Newsroom'),
            )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class SocialNewsroom(Container):
    grok.implements(ISocialNewsroom)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# social_newsroom_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SocialView(grok.View):
    """ sample view class """

    grok.context(ISocialNewsroom)
    grok.require('zope2.View')

    def update(self):
        fc = self.context.listFolderContents()
        folderobjects = []
        for i in fc:
            obj = {}
            obj['title'] = i.title
            obj['description'] = i.description
            obj['socialcontent'] = i.getSocialContent()
            folderobjects.append(obj)

        self.folderobjects = folderobjects
        self.text = self.context.details.output



