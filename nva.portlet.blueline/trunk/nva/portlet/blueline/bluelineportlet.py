from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from nva.portlet.blueline import BlueLinePortletMessageFactory as _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

class IBlueLinePortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    portlettitle = schema.TextLine(title=_(u"Titel des Portlets"),
                                   description=_(u"Wenn gewuenscht geben Sie hier bitte eine Ueberschrift fuer das Portlet an."),
                                   required = False,
                                  )

    portletcontent = schema.List(title=_(u"Portletinhalt"),
                           description=_(u"Titel im Portlet@pfad_im_portal_oder_URL (Beispiel: Suche@http://www.google.de"),
                           value_type=schema.TextLine(),
                           required=True)

    portletfooter = schema.TextLine(title=_(u"Fusszeile des Portlets"),
                                    description=_(u"Wenn gewuenscht geben Sie hier bitte die Fusszeile des Portlets an."),
                                    required=False,
                                    )

    footerurl = schema.TextLine(title=_(u"Pfad oder URL"),
                                description=_(u"Bitte geben Sie hier den Pfad oder die URL an, mit der die Fusszeile verlinkt werden soll"),
                                required=False,
                               )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBlueLinePortlet)

    # TODO: Set default values for the configurable parameters here

    portlettitle = u""
    portletcontent = []
    portletfooter = u""
    footerurl = u""

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, portlettitle=u"", portletcontent=[], portletfooter=u"", footerurl=""):
        self.portlettitle = portlettitle
        self.portletcontent = portletcontent
        self.portletfooter = portletfooter
        self.footerurl = footerurl

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"Blueline Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('bluelineportlet.pt')

    def portletcontent(self):
        data = {'title':self.data.portlettitle,
                'contents':[i.split('@') for i in self.data.portletcontent],
                'footer':self.data.portletfooter,
                'footerurl':self.data.footerurl,
               }
        return data


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IBlueLinePortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IBlueLinePortlet)
