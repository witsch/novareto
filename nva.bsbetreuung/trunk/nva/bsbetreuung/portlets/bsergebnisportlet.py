from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from nva.onlinehandlungshilfe.lib.xlsreader import xlsreader
from nva.onlinehandlungshilfe.lib.calculator import calculate_gb
from nva.onlinehandlungshilfe.lib.calculator import calculate_sb
from nva.onlinehandlungshilfe.lib.calculator import calculate_step

from nva.bsbetreuung import bsbetreuungMessageFactory as _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

daten = xlsreader()
main = daten['main']

class IBSErgebnisPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    portlettitle = schema.TextLine(title=_(u"Titel der Ergebnisportlets"),
                                    description=_(u"Bitte tragen Sie hier einen Titel fuer das Portlet ein"),
                                    required=True,)

    link_ma = schema.TextLine(title=_(u"Ordner Handlungshilfe"),
                              description=_(u"Bitte tragen Sie hier den Pfad zur Startseite der Online Handlungshilfe ein."),
                              required=True,)

    link_gb = schema.TextLine(title=_(u"Ordner Grundbetreuung"),
                              description=_(u"Bitte tragen Sie hier den Pfad zum Ordner fuer die Grundbetreuung ein."),
                              required=True,)

    link_sb = schema.TextLine(title=_(u"Ordner Betriebsspezifische Betreuung"),
                              description=_(u"Bitte tragen Sie hier den Pfad zum Ordner fuer die Betriebsspezifische Betreuung ein."),
                              required=True,)

    final_step_sb = schema.TextLine(title=_(u"Letzte Seite des Wizards Betriebsspezifische Betreuung"),
                                    description=_(u"Bitte tragen Sie hier die letzte Seite des Wizards fuer die betriebsspezifische Betreuung ein."),
                                    required=True,)

    moreinfo = schema.TextLine(title=_(u"Weitergehende Informationen"),
                                    description=_(u"Bitte tragen Sie hier die URL zur Seite mit den weitergehenden Informationen ein."),
                                    required=True,)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBSErgebnisPortlet)

    # TODO: Set default values for the configurable parameters here

    portlettitle = "Ergebnis Portlet"
    final_step_sb = "3"
    moreinfo = ""
    link_ma = ""
    link_gb = ""
    link_sb = ""

    def __init__(self, portlettitle=u"", final_step_sb=u"", moreinfo=u"", link_ma="", link_gb="", link_sb=""):
        self.final_step_sb = final_step_sb
        self.portlettitle = portlettitle
        self.moreinfo = moreinfo
        self.link_ma = link_ma
        self.link_gb = link_gb
        self.link_sb = link_sb

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"BS-Ergebnis Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('bsergebnisportlet.pt')

    def results(self):
        """returns the actual resultset of online-handlungshilfe"""

        session_manager = self.context.session_data_manager
        session = session_manager.getSessionData()

        #Daten fuer den Mitarbeiter
        data_startseite = session.get('start', {})
        mitarbeiter = data_startseite.get('mitarbeiter',0)
        if mitarbeiter == 0:
            mitarbeiter = self.request.get('mitarbeiter',0)
        elif self.request.get('resetstart',''): #Portlet bei Reset sofort loeschen
            mitarbeiter = 0

        #Daten fuer die Grundbetreuung
        data_grundbetreuung = session.get('gb', {})
        step = data_grundbetreuung.get('gb_steps', '')
        wz_code = ''
        aufwand_gb = 0.0
        wz_code = data_grundbetreuung.get('wzcodenr', '')
        if not wz_code:
            wz_code = self.request.get('gb_step%s' %step, '')

        faktor = main.get(wz_code, {}).get('faktor', 0)
        if faktor != 0:
            aufwand_gb = calculate_gb(mitarbeiter, faktor)
            aufwand_gb = round(aufwand_gb,1)
            aufwand_gb = "%.1f" %aufwand_gb
            aufwand_gb = aufwand_gb.replace('.',',')
        else:
            wz_code = ''

        if self.request.get('resetgb',''): #Portlet bei Reset sofort loeschen
            wz_code = ''
            aufwand_gb = 0.0

        #Daten fuer die betriebsspezifische Betreuung
        data_spezbetreuung = session.get('sb', {})
        summe_sb = data_spezbetreuung.get('sbsum', 0.0)

        if data_spezbetreuung and summe_sb < 2.0:
            summe_sb = 2.0

        aufwand_sb = "%.1f" %summe_sb
        aufwand_sb = aufwand_sb.replace('.',',')

        if self.request.get('resetsb',''): #Portlet bei Reset sofort loeschen
            aufwand_sb = 0.0

        resultset = {'portlettitle':self.data.portlettitle,
                     'mitarbeiter':mitarbeiter,
                     'wz_code':wz_code,
                     'aufwand_gb':aufwand_gb,
                     'aufwand_sb':aufwand_sb,
                     'moreinfo':self.data.moreinfo,
                     'link_ma':"%s/%s" %(self.context.portal_url(),self.data.link_ma),
                     'link_gb':"%s/%s" %(self.context.portal_url(),self.data.link_gb),
                     'link_sb':"%s/%s" %(self.context.portal_url(),self.data.link_sb),
                    }

        if mitarbeiter == 0 and not wz_code and aufwand_gb == 0.0 and aufwand_sb == '0,0':
            resultset = {}

        return resultset


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IBSErgebnisPortlet)

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
    form_fields = form.Fields(IBSErgebnisPortlet)
