# -*- coding: utf-8 -*-
try:
    import ldap
except:
    print "+++ Auf diesem System wird kein LDAP unterstuetzt +++"
import smtplib
import mimetypes
from time import gmtime, strftime
from email import Encoders
from email.Message import Message
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from os import system
from App.config import getConfiguration
from nva.visitor import visitorMessageFactory as _

config = getConfiguration()
try:
    configuration = config.product_config.get('visitor', dict())
    ldapserver = configuration.get('ldapserver')
    ldapadmin = configuration.get('ldapadmin')
    ldappassw = configuration.get('ldappassw')
    basedn = configuration.get('basedn')
    mailserver = configuration.get('mailserver')
    tmpfile = configuration.get('tmpfile')
except:
    ldapserver = 'rs-aug-bendc-01.pfister.de'
    ldapadmin = "cn=svc-agb-plonedummy,ou=systemkonten,dc=pfister,dc=de"
    ldappassw = "xxxxxxxxxx"
    basedn = "ou=user,ou=Pfister GmbH,dc=pfister,dc=de"
    mailserver = 'rs-aug-appsv-01'
    tmpfile = '/tmp'

def ldapsearch(sfilter=None):
    """Sucht im ActiveDirectory der Firma Pfister"""

    l = ldap.open(ldapserver)
    l.protocol_version = ldap.VERSION3
    l.simple_bind_s(ldapadmin,ldappassw)
    if sfilter:
        res = l.search_s(basedn, ldap.SCOPE_SUBTREE, sfilter)
    else:
        res = l.search_s(basedn, ldap.SCOPE_SUBTREE)
    return res


def sMail(to,sender,subject,text,url):
    """SEND A MAIL"""

    empfaenger=to
    absender=sender
    betreff=subject
    text=text

    msg="To: %s\n" %empfaenger
    msg=msg+"From: %s\n" %absender
    msg=msg+"Subject: %s\n\n" %betreff
    msg=msg+text
    msg=msg+url

    server = smtplib.SMTP(mailserver)
    server.sendmail(absender, empfaenger,msg)
    server.close()
    return


def iCalFile(msg,subject,url,startdate,enddate,location,mailfrom,mailto,recips):
    """SEND A MAIL WITH VCAL-FILE in ATTACHMENT"""

    msg1 = u'Folgender Termin wurde neu im Intranet eingetragen.\n'
    msg1 = msg1 + u'Durch Aufruf und Speichern des Anhanges können Sie den Termin in Ihren Kalender übernehmen.:\n\n'
    msg1 = msg1 + u'%s\n\n' %subject
    msg1 = msg1 + u'Zeit: von %s bis %s\n' %(startdate,enddate)
    msg1 = msg1 + u'Ort: %s\n' %location
    msg1 = msg1 + u'Absender: mailto:%s\n' %mailfrom
    msg1 = msg1 + u'Link zum Besuchstermin im Intranet: %s' %url

    timestamp=strftime("%Y%m%dT%H%M%S")
    dateiname = "%sBesuchstermin" %tmpfile
    dateiname = dateiname+timestamp+".ics"
      
    start=startdate[0:4]+startdate[5:7]+startdate[8:10]+'T'+startdate[11:13]+startdate[14:16]+startdate[17:19]
    end=enddate[0:4]+enddate[5:7]+enddate[8:10]+'T'+enddate[11:13]+enddate[14:16]+enddate[17:19]

    x=open(dateiname,'w')
    textlines = [
        'BEGIN:VCALENDAR\n',
        'PRODID:-//PloneCommunity//Plone 2.04 MIMEDIR//EN\n',
        'VERSION:2.0\n',
        'METHOD:PUBLISH\n',
        'BEGIN:VEVENT\n',
        'ATTENDEE;ROLE=REQ-PARTICIPANT;RSVP=TRUE:MAILTO:%s\n' %recips,
        'ORGANIZER:MAILTO:%s\n' %mailfrom,
        'DTSTART:%s\n' %start,
        'DTEND:%s\n' %end,
        'LOCATION:%s\n' %location,
        'TRANSP:OPAQUE\n',
        'SEQUENCE:0\n',
        'UID:%s\n' %timestamp,
        'DTSTAMP:%s\n' %timestamp,
        'DESCRIPTION:%s\n' %msg,
        'SUMMARY:%s\n' %subject,
        'CLASS:PUBLIC\n',
        'BEGIN:VALARM\n',
        'ACTION:DISPLAY\n',
        'DESCRIPTION:Reminder\n',
        'END:VALARM\n',
        'END:VEVENT\n',
        'END:VCALENDAR\n',
        ]

    for i in textlines:
        x.write(i)

    x.close()
    sender = mailfrom
    body = msg1
    outer = MIMEMultipart()
    outer['Subject'] = 'Neuer Eintrag im Besuchskalender'
    outer['To'] = recips
    outer['From'] = sender
    outer['message'] = 'Neuer Besuchstermin im Intranet'
    outer.attach(MIMEText(body.encode('utf-8'), _charset='utf-8'))
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    outer.epilogue = ''
    path = dateiname
    filename = "Besuchstermin.ics"
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    fp = open(path, 'rb')
    msg = MIMEBase(maintype, subtype)
    msg.set_payload(fp.read())
    fp.close()
    Encoders.encode_base64(msg)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    outer.attach(msg)
    MailHost=mailserver
    s=smtplib.SMTP()
    s.connect(MailHost)
    s.sendmail(mailfrom, mailto, outer.as_string())
    s.close()
    befehl='del %s' %dateiname
    system(befehl)


def iCalCancel(msg,subject,url,startdate,enddate,location,mailfrom,mailto,recips):
    msg1 = u'Bitte löschen Sie bei Bedarf folgenden Termin in Ihrem Kalender:\n\n'
    msg1 = msg1 + u'%s\n\n' %subject
    msg1 = msg1 + u'Zeit: von %s bis %s\n' %(startdate,enddate)
    msg1 = msg1 + u'Ort: %s\n' %location
    msg1 = msg1 + u'Absender: mailto:%s\n' %mailfrom
    sender = mailfrom
    body = msg1
    outer = MIMEMultipart()
    outer['Subject'] = u'Achtung: Termin im Besuchskalender wurde zurückgezogen'
    outer['To'] = recips
    outer['From'] = sender
    outer['message'] = u'Besuchstermin wurde zurückgezogen'
    outer.attach(MIMEText(body.encode('utf-8'), _charset='utf-8'))
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    outer.epilogue = ''
    MailHost=mailserver
    s = smtplib.SMTP()
    s.connect(MailHost)
    s.sendmail(mailfrom, mailto, outer.as_string())
    s.close()

