import grok

from loginserver import resource
from zope.interface import Interface
from zope.schema import TextLine, Password
from M2Crypto import RSA
import auth_pubtkt
import time, datetime
import os.path
import loginserver
from urllib import quote
import base64
import xmlrpclib
from grokcore.message import receive


privkey_path = os.path.join(os.path.dirname(loginserver.__file__), 'privkey.pem')
privkey = RSA.load_key(privkey_path)


class Loginserver(grok.Application, grok.Container):
    pass


class Index(grok.View):

    def update(self, login=None, password=None, anmelden=None):
        if not anmelden:
            return
        if not self.checkRule(login, password):
            return
        if self.checkAuth(login, password) == 0:
            self.flash(u'Benutzername und oder Passwort nicht richtig')
            return
        request = self.request
        val = base64.encodestring('%s:%s' % (login, password))
        validuntil = int(time.mktime(datetime.datetime(2012, 4, 1).timetuple()))
        ticket = auth_pubtkt.create_ticket(privkey, '0000-00025', validuntil, tokens=['su'])
        request.response.setHeader(
            'Set-Cookie:', 
            'auth_pubtkt=%s;domain=novareto.de;path=/' % quote(ticket))
        request.response.setCookie(
            'dolmen.authcookie', 
            quote(val), 
            path="/", 
            domain="novareto.de")
        # Flash Messages
        return request.response.redirect('http://extranet.novareto.de', trusted=True)

    def checkRule(self, login, password):
        return True

    def checkAuth(self, login, password):
        server = "http://192.168.2.167:8080/app"
        portal = xmlrpclib.Server(server)
        return portal.checkAuth(login, password)

    @property
    def messages(self):
        received = receive()
        if received is not None:
            messages = list(received)
        else:
            messages = []
        return messages
