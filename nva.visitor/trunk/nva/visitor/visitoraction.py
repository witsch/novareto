# -*- coding: utf-8 -*-
from persistent import Persistent 
from OFS.SimpleItem import SimpleItem

from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema
from zope.app.component.hooks import getSite

from zope.component.interfaces import IObjectEvent
from Products.CMFCore.utils import getToolByName

from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData

from plone.app.contentrules.browser.formhelper import AddForm, EditForm 

from Acquisition import aq_inner

from nva.visitor.lib.helpers import usermail, iCalFile
from nva.visitor import visitorMessageFactory as _

class IVisitorSendAction(Interface):
    """Interface zur Konfiguration eines List-Feldes mit Empfaengern.
    """
    
    empfaenger = schema.List(title=_(u"Empfaenger"),
                            description=_(u"Hier koennen Sie eine Liste mit statischen Empfaengern der Mail konfigurieren."),
                            required=True,
                            value_type=schema.TextLine(title=_(u"Mailadresse"))
                            )

class VisitorSendAction(SimpleItem):
    """Test """
    implements(IVisitorSendAction, IRuleElementData)

    empfaenger = []    
    element = "nva.visitor.visitoraction"

    def summary(self):
        return _(u"Empfaengerliste: ${myempfaenger}", mapping=dict(myempfaenger=", ".join(self.empfaenger)))


class VisitorSendActionExecutor(object):
    """Test """
    implements(IExecutable)
    adapts(Interface, IVisitorSendAction, IObjectEvent)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        context = aq_inner(self.event.object)
        ploneutils = getToolByName(self.context, 'plone_utils')
        portal_membership = getToolByName(self.context, 'portal_membership')

        obj = self.event.object

        name = portal_membership.getAuthenticatedMember().id

        try:
            sender = usermail(name=name)
        except:
            sender = 'intranet@FLSmidthPfister.com'

        vliste=[]
        vstrng=''

        for i in obj.getMailing():
            if i:
                vliste.append(i)
                if vstrng:
                    vstrng=vstrng + ', <' + i + '>'
                else:
                    vstrng=vstrng + '<' + i + '>'

        to=vliste

        cc=[]
        for i in self.element.empfaenger:
            cc.append(i)

        title = obj.Title()
        url = obj.absolute_url()
        startdate = str(obj.getStartdate())
        enddate = str(obj.getEnddate())
        location = obj.getMylocation()

        firma=obj.getFirma()
        ortland=obj.getOrtland()
        apart=obj.getAnsprechpartner()
        grund=obj.getGrund()
        gespraecht=str(obj.getGespraechsteilnehmer()).replace('\x0D', ',').replace('\x0A', ' ')

        #Unterschied zwischen Besucher und Bewerber(1)
        if obj.portal_type == "Besuchsanmeldung":
            brancheakt=obj.getBrancheaktivitaeten()
            geschaeft=obj.getGbeziehung()


        msg = u'Zeit: von %s bis %s\\n' %(startdate,enddate)
        msg = msg + u'  Ort: %s\\n' %location
        msg = msg + u'  Absender: mailto:%s\\n' %sender
        msg = msg + u'  Link zum Besuchstermin im Intranet: %s\\n\\n' %url
        msg = msg + u'  Firma des Besuchers: %s\\n' %firma
        msg = msg + u'  Ort/Land des Besuchers: %s\\n' %ortland
        msg = msg + u'  Ansprechpartner: %s\\n' %apart
        msg = msg + u'  Grund des Besuches: %s\\n' %grund

        #Unterschied zwischen Besucher und Bewerber(2)
        if obj.portal_type == "Besuchsanmeldung":
            msg = msg + u'  Branche/Aktivitäten: %s\\n' %brancheakt
            msg = msg + u'  Geschäftsbeziehung: %s\\n' %geschaeft

        if gespraecht is not None:
                msg = msg + u'  Gesprächsteilnehmer: %s\\n' %gespraecht


        #Unterschied zwischen Besucher und Bewerber(3)
        if obj.portal_type == "Besuchsanmeldung":
            a=obj.setExpirationDate(obj.getEnddate() + 1)

        subject=u' %s' %title

        try:
            if sender != '':
                if vliste != []:
                    m=iCalFile(msg,subject,url,startdate,enddate,location,sender,vliste,vstrng)
                m=iCalFile(msg,subject,url,startdate,enddate,location,sender,cc,cc_str)
            msg = _(u"Mail mit Termindaten wurde versendet")

        except:
            msg = _(u"Mail mit Termindaten konnte auf Grund eines Fehlers nicht versendet werden.")
        ploneutils.addPortalMessage(msg)
        self.context.REQUEST.response.redirect(obj.absolute_url())

        return True

class VisitorSendActionAddForm(AddForm):
    """Portal-Form fuer das Anlegen der Action
    """
    form_fields = form.FormFields(IVisitorSendAction)
    label = _(u"Konfiguration des Mailversandes bei Besuchern oder Bewerbern.")
    description = _(u"Hier kann eine statische Liste mit Empfaengern fuer den Mailversand angegeben werden.")
    form_name = _(u"Configure element")

    def create(self, data):
        c = VisitorSendAction()
        form.applyChanges(c, self.form_fields, data)
        return c

class VisitorSendActionEditForm(EditForm):
    """Plone-Form fuer die Bearbeitung der Action
    """
    form_fields = form.FormFields(IVisitorSendAction)
    label = _(u"Bearbeitung des Mailversandes")
    description = _(u"Bearbeitung der statischen Liste mit Empfaengern von Besucher- und Bewerberterminen.")
    form_name = _(u"Configure element")

