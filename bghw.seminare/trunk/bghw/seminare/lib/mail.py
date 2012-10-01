# -*- coding: utf-8 -*-
import smtplib
import mimetypes
from email import Encoders
from email.Message import Message
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText

def sMail(mailserver, to, sender, cc, subject, text, pdfdata, filename, reply=None):
        """SEND A MAIL TO UNFALLANZEIGE MAILBOX"""

        import smtplib
        import mimetypes
        from email import Encoders
        from email.Message import Message
        from email.MIMEAudio import MIMEAudio
        from email.MIMEBase import MIMEBase
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEImage import MIMEImage
        from email.MIMEText import MIMEText

        empfaenger=to
        print 'mailto: '+empfaenger

        absender=sender
        print 'mailfrom: '+absender

        kopie=cc
        print 'CC: '+kopie

        betreff=subject
        print 'Betreff: ',betreff

        msg="To: %s\n" %empfaenger
        msg=msg+"From: %s\n" %absender
        if reply:
            msg=msg+"Reply-To: %s\n" %reply
        msg=msg+"Subject: %s\n\n" %betreff
        msg=msg+text

        body=msg
        outer=MIMEMultipart()
        outer['Subject']=betreff
        outer['To']=empfaenger
        outer['From']=absender
        if reply:
            outer['Reply-to']=reply
        outer['message']=text
        outer.attach(MIMEText(body.encode('utf-8'), _charset='utf-8'))
        outer.preamble='You will not see this in a MIME-aware mail reader.\n'
        outer.epilogue=''
        ctype, encoding=mimetypes.guess_type(pdfdata)
        if ctype is None or encoding is not None:
                ctype='application/octet-stream'
        print ctype, encoding
        maintype, subtype = ctype.split('/',1)
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(pdfdata)
        Encoders.encode_base64(msg)
        msg.add_header('Content-Disposition','attachement', filename=filename)
        outer.attach(msg)

        try:
            server = smtplib.SMTP(mailserver)
            server.sendmail(absender, empfaenger, outer.as_string())
            if kopie:
                server.sendmail(absender, kopie, outer.as_string())
            server.close()
        except:
            print 'Mailserver gestoert!'

        return None
