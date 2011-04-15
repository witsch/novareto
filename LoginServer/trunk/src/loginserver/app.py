
import auth_pubtkt
import datetime
import base64
import grok
import time
import xmlrpclib
import zope.app.appsetup.product


from M2Crypto import RSA
from grokcore.message import receive
from urllib import quote


config = zope.app.appsetup.product.getProductConfiguration('loginserver')

privkey = RSA.load_key(config.get('private_key_path'))


class Loginserver(grok.Application, grok.Container):
    pass


class Index(grok.View):

    def update(self, login=None, password=None, anmelden=None):
        if not anmelden:
            return
        if not self.checkRule(login, password):
            return
        if self.checkAuth(login, password) == 0:
            self.flash(config.get('wrong_credentials'))
            return

        request = self.request
        val = base64.encodestring('%s:%s' % (login, password))
        validuntil = int(time.mktime(
            datetime.datetime(2012, 4, 1).timetuple()))
        ticket = auth_pubtkt.create_ticket(
            privkey, login, validuntil, tokens=['su'])
        request.response.setHeader(
            'Set-Cookie',
            'auth_pubtkt=%s;domain=%s;path=/; Secure' % (
            quote(ticket),
            config.get('cookie_domain')))
        request.response.setCookie(
            'dolmen.authcookie',
            quote(val),
            path="/",
            secure=True,
            domain=config.get('cookie_domain'))
        return request.response.redirect(config.get('backurl'), trusted=True)

    def checkRule(self, login, password):
        return True

    def checkAuth(self, login, password):
        server = "http://10.30.4.78:8888/app"
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
