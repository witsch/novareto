import os
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

from M2Crypto import EVP
import StringIO

iv = os.urandom(16)




class Index(grok.View):

    def bauth(self, val):

        def encrypt(data, key):
            # Zero padding
            if len(data) % 16 != 0:
                data += '\0' * (16 - len(data) % 16);
            buffer = StringIO.StringIO()
            cipher = EVP.Cipher('aes_128_cbc', key=key, iv=iv, op=1)
            cipher.set_padding(0)
            buffer.write(cipher.update(str(data)))
            buffer.write(cipher.final())
            data = iv + buffer.getvalue()
            print "DATA", data
            return data
        return encrypt(val, '1234567890ABCDEF')


    def update(self, login=None, password=None, anmelden=None):
        if not anmelden:
            return
        if not self.checkRule(login, password):
            return
        if self.checkAuth(login, password) == 0:
            self.flash(config.get('wrong_credentials'))
            return

        request = self.request
        val = base64.encodestring(self.bauth('%s:%s' % (login, password)))
        validuntil = int(time.mktime(
            datetime.datetime(2012, 12, 1).timetuple()))
        print val
        ticket = auth_pubtkt.create_ticket(
                privkey, login, validuntil, tokens=['su'], extra_fields=(('bauth', val),))
        request.response.setHeader(
            'Set-Cookie',
            'auth_pubtkt=%s;domain=%s;path=/;' % (
            quote(ticket),
            config.get('cookie_domain')))

        #request.response.setCookie(
        #    'dolmen.authcookie',
        #    quote(val),
        #    path="/",
        #    secure=False,
        #    domain=config.get('cookie_domain'))

        print "SETET COOKIE", ticket
        return request.response.redirect(config.get('backurl'), trusted=True)

    def checkRule(self, login, password):
        return True

    def checkAuth(self, login, password):
        if login == "admin" and password == "admin":
            return 1
        return

    @property
    def messages(self):
        received = receive()
        if received is not None:
            messages = list(received)
        else:
            messages = []
        return messages
