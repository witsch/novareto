import smtplib
import mimetypes
from email import Encoders
from email.Message import Message
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
import string

mailserver='193.104.3.40'


def sMail(to,sender,cc,subject,text,path,filename):
    """SEND A MAIL TO UNFALLANZEIGE MAILBOX"""

    empfaenger=to
    print 'mailto: '+empfaenger

    absender=sender
    print 'mailfrom: '+absender

    kopie=cc
    print 'kopie: '+kopie

    betreff=subject
    text=text

    #msg="To: %s\n" %empfaenger
    #msg=msg+"From: %s\n" %absender
    #msg=msg+"Subject: %s\n\n" %betreff
    #msg=msg+text
    msg = text

    body=msg
    outer=MIMEMultipart()
    outer['Subject']=betreff
    outer['To']=empfaenger
    outer['From']=absender
    outer['message']="Bitte beachten Sie das Dokument im Anhang zur Mail."
    outer.attach(MIMEText(body.encode('utf-8'), _charset='utf-8'))
    outer.preamble='You will not see this in a MIME-aware mail reader.\n'
    outer.epilogue=''
    ctype, encoding=mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
            ctype='application/octet-stream'
    maintype, subtype = ctype.split('/',1)
    fp = open(path,'rb')
    msg = MIMEBase(maintype, subtype)
    msg.set_payload(fp.read())
    fp.close()
    Encoders.encode_base64(msg)
    msg.add_header('Content-Disposition','attachement', filename=filename)
    outer.attach(msg)

    server = smtplib.SMTP(mailserver)
    server.set_debuglevel(0)
   
    server.sendmail(absender, empfaenger, outer.as_string())
    #server.sendmail(absender, kopie, outer.as_string())

    server.close()

    return None

