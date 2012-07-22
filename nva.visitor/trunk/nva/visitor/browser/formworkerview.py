# -*- coding: utf-8 -*-
from DateTime import DateTime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from nva.visitor import visitorMessageFactory as _
from nva.visitor.lib.helpers import ldapsearch, iCalFile, iCalCancel

class IformworkerView(Interface):
    """
    formworker view interface
    """

    def test():
        """ test method"""


class formworkerView(BrowserView):
    """
    formworker browser view
    """
    implements(IformworkerView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def usermail(self, name):
        """sucht die Mailadresse eines Benutzers aus LDAP"""
        return "rudi.cerne@zdf.de"
        sfilter = "(sn=%s)" %name
        res = ldapsearch(sfilter)
        ldapmail = 'intranetmaster@pfister.de'
        if res:
            for entry in res:
                if entry[1].has_key('mail'):
                    ldapmail = entry[1].get('mail')[0]
        return ldapmail

    def pfister_send(self):
        """ send Mail """

        name = self.portal_membership.getAuthenticatedMember().id
        sender=self.usermail(name=name)

        vliste=[]
        vstrng=''

        for i in self.context.getMailing():
            if i:
                vliste.append(i)
                if vstrng:
                    vstrng=vstrng + ', <' + i + '>'
                else:
                    vstrng=vstrng + '<' + i + '>'

        to=vliste
        cc_str='verteilerbesucher@FLSmidthPfister.com'
        cc=[]
        cc.append(cc_str)

        title = self.context.Title()
        url = self.context.absolute_url()
        startdate = str(self.context.getStartdate())
        enddate = str(self.context.getEnddate())
        location = self.context.getMylocation()

        firma=self.context.getFirma()
        ortland=self.context.getOrtland()
        brancheakt=self.context.getBrancheaktivitaeten()
        geschaeft=self.context.getGbeziehung()
        apart=self.context.getAnsprechpartner()
        grund=self.context.getGrund()
        gespraecht=str(self.context.getGespraechsteilnehmer()).replace('\x0D', ',').replace('\x0A', ' ')

        msg = u'Zeit: von %s bis %s\\n' %(startdate,enddate)
        msg = msg + u'  Ort: %s\\n' %location
        msg = msg + u'  Absender: mailto:%s\\n' %sender
        msg = msg + u'  Link zum Besuchstermin im Intranet: %s\\n\\n' %url
        msg = msg + u'  Firma des Besuchers: %s\\n' %firma
        msg = msg + u'  Ort/Land des Besuchers: %s\\n' %ortland
        msg = msg + u'  Branche/Aktivitäten: %s\\n' %brancheakt
        msg = msg + u'  Geschäftsbeziehung: %s\\n' %geschaeft
        msg = msg + u'  Ansprechpartner: %s\\n' %apart
        msg = msg + u'  Grund des Besuches: %s\\n' %grund
        if gespraecht is not None:
                msg = msg + u'  Gesprächsteilnehmer: %s\\n' %gespraecht

        a=self.context.setExpirationDate(self.context.getEnddate() + 1)
        subject=' %s' %title
        if sender != '':
                if vliste != []:
                        m=iCalFile(msg,subject,url,startdate,enddate,location,sender,vliste,vstrng)
                m=iCalFile(msg,subject,url,startdate,enddate,location,sender,cc,cc_str)

    def pfister_cancel(self):
        """ send Mail """

        name = self.portal_membership.getAuthenticatedMember().id
        sender=self.usermail(name=name)

        vliste=[]
        vstrng=''

        for i in self.context.getMailing():
            if i:
                 vliste.append(i)
                 if vstrng:
                     vstrng=vstrng + ', <' + i + '>'
                 else:
                     vstrng=vstrng + '<' + i + '>'

        to=vliste
        cc_str='verteilerbesucher@FLSmidthPfister.com'
        cc=[]
        cc.append(cc_str)

        title = self.context.Title()
        url = self.context.absolute_url()
        startdate = str(self.context.getStartdate())
        enddate = str(self.context.getEnddate())
        location = self.context.getMylocation()

        firma=self.context.getFirma()
        ortland=self.context.getOrtland()
        brancheakt=self.context.getBrancheaktivitaeten()
        geschaeft=self.context.getGbeziehung()
        apart=self.context.getAnsprechpartner()
        grund=self.context.getGrund()
        gespraecht=str(self.context.getGespraechsteilnehmer()).replace('\x0D', ',').replace('\x0A', ' ')

        msg = u'Zeit: von %s bis %s\\n' %(startdate,enddate)
        msg = msg + u'  Ort: %s\\n' %location
        msg = msg + u'  Absender: mailto:%s\\n' %sender
        msg = msg + u'  Link zum Besuchstermin im Intranet: %s\\n\\n' %url
        msg = msg + u'  Firma des Besuchers: %s\\n' %firma
        msg = msg + u'  Ort/Land des Besuchers: %s\\n' %ortland
        msg = msg + u'  Branche/Aktivitäten: %s\\n' %brancheakt
        msg = msg + u'  Geschäftsbeziehung: %s\\n' %geschaeft
        msg = msg + u'  Ansprechpartner: %s\\n' %apart
        msg = msg + u'  Grund des Besuches: %s\\n' %grund
        if gespraecht is not None:
                msg = msg + u'  Gesprächsteilnehmer: %s\\n' %gespraecht

        subject=' %s' %title
        if sender != '':
                if vliste != []:
                        m=iCalCancel(msg,subject,url,startdate,enddate,location,sender,vliste,vstrng)
                m=iCalCancel(msg,subject,url,startdate,enddate,location,sender,cc,cc_str)


    def __call__(self):
        """Ausfuehrung der Aktion"""
        if self.request.get('button.senden'):
            self.context.mailsent = True
            self.pfister_send()
        elif self.request.get('button.cancel'):
            self.context.mailsent = False
            self.pfister_cancel()
        return self.request.response.redirect(self.context.absolute_url())

