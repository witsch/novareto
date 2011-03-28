import grok

from loginserver import resource
from zope.interface import Interface
from zope.schema import TextLine, Password
from M2Crypto import RSA
import auth_pubtkt
import time, datetime
import os.path
import loginserver


privkey_path = os.path.join(os.path.dirname(loginserver.__file__), 'privkey.pem')
privkey = RSA.load_key(privkey_path)



class ILogin(Interface):

    login = TextLine(title=u"Login")
    password = Password(title=u"Password")



class Loginserver(grok.Application, grok.Container):
    pass

class Index(grok.Form):

    form_fields = grok.AutoFields(ILogin)

    @grok.action(u'Anmelden')
    def handle_anmelden(self, **data):
        request = self.request
        validuntil = int(time.mktime(datetime.datetime(2012, 4, 1).timetuple()))
        ticket = auth_pubtkt.create_ticket(privkey, '0101010001', validuntil, tokens=['su'])
        request.response.setCookie('auth_pubtkt', ticket, path="/", domain="novareto.de")
        return request.response.redirect('http://extranet.novareto.de', trusted=True)
