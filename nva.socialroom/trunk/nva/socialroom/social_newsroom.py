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

class ISocialNewsroom(form.Schema, IImageScaleTraversable):
    """
    A Folder to accumulate content from social networks.
    """

    details = RichText(
            title = _(u'Beschreibung der Details zum Newsroom'),
            )

class SocialNewsroom(Container):
    grok.implements(ISocialNewsroom)


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
            obj['url'] = i.absolute_url()
            obj['description'] = i.description
            obj['socialcontent'] = i.getSocialContent()
            folderobjects.append(obj)

        self.folderobjects = folderobjects
        self.text = self.context.details.output
