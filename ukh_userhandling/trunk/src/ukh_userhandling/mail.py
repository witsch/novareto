# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import zope.app.appsetup.product
import zope.component
import zope.sendmail.delivery
import zope.sendmail.interfaces
import zope.sendmail.mailer
import zope.sendmail.queue
import email.MIMEText
import email.Header


from email.MIMEBase import MIMEBase
from email import Encoders
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE


queue_path = "/tmp/mailequeue" 
hostname = "10.64.33.11" 
port = 25
username = None
password = None

mailer_object = zope.sendmail.mailer.SMTPMailer(
        hostname, port, username, password, force_tls=False)


def mailer():
    return mailer_object


def delivery():
    return zope.sendmail.delivery.QueuedMailDelivery(queue_path)


def start_processor_thread():
    thread = zope.sendmail.queue.QueueProcessorThread()
    thread.setMailer(mailer_object)
    thread.setQueuePath(queue_path)
    thread.start()


def send_mail(sender, recipient, subject, body, file=None):
    '''
    Funktion zum versenden von Emails
    recipient muss als Liste übergeben werden
    body sollte einen formatierter String sein
    '''
   
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = COMMASPACE.join(recipient)  # List to String
    msg["Subject"] = email.Header.Header(subject, 'UTF-8')
    msg.attach(MIMEText(body.encode('utf-8'),'plain','utf-8'))
   
    # Attachment von Dateien
    if file!=None:
        filename = file.split("/")
        filename = filename[-1]
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', 
            'attachment; filename=%s' % filename
            )
        msg.attach(part)
    mailer = zope.component.getUtility(
        zope.sendmail.interfaces.IMailDelivery, 
        name=u'uvcsite.maildelivery'
        )
    mailer.send(sender, recipient, msg.as_string())


grok.global_utility(
    mailer,
    provides=zope.sendmail.interfaces.IMailer,
    name='uvcsite.smtpmailer')
grok.global_utility(
    delivery,
    zope.sendmail.interfaces.IMailDelivery,
    name='uvcsite.maildelivery')
start_processor_thread()
