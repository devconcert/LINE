# -*- coding: utf-8 -*-
"""
    line.client
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re
import rsa
import requests
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

from linethrift import LineThrift

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['LineClient']

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class LineClient(object):
    """This class proviede you a way to communicate with LINE server.

    :param email: NAVER id or NAVER email
    :param password: LINE password
    """

    LINE_DOMAIN = "http://gd2.line.naver.jp"

    LINE_HTTP_URL        = LINE_DOMAIN + "/api/v4/TalkService.do"
    LINE_SESSION_URL     = LINE_DOMAIN + "/authct/v1/keys/line"
    LINE_CERTIFICATE_URL = LINE_DOMAIN + "/Q"

    ip          = "127.0.0.1"
    version     = "3.7.0"
    com_name   = "carpedm20"

    _session = requests.session()
    _headers = {}

    def __init__(self, id, password, is_mac=True):
        """Initialize LINE instance with provided information

        :param id: `NAVER id` or `LINE e-mail`
        :param password: LINE account password
        """
        self.id = id
        self.password = password
        self.is_mac = is_mac

        self._login()
        
        print "Enter PinCode '%s' to your mobile phone" % self._pinCode

    def get_json(self, url):
        return json.loads(self._session.get(url, headers=self._headers).text)

    def login(self):
        j = self.get_json(self.LINE_CERTIFICATE_URL)
        self.verifier = j['result']['verifier']

        msg = self.client.loginWithVerifierForCertificate(self.verifier)
        print msg

    def _login(self):
        """Login to LINE server."""
        if EMAIL_REGEX.match(self.id):
            self.provider = 1
        else:
            self.provider = 2

        if self.is_mac:
            os_version  = "10.9.4-MAVERICKS-x64"
            user_agent  = "DESKTOP:MAC:%s(%s)" % (os_version, self.version)
            application = "DESKTOPMAC\t%s\tMAC\t%s" % (self.version, os_version)
        else:
            os_version  = "5.1.2600-XP-x64"
            user_agent  = "DESKTOP:WIN:%s(%s)" % (os_version, self.version)
            application = "DESKTOPWIN\t%s\tWINDOWS\t%s" % (self.version, os_version)

        self._headers['User-Agent']         = user_agent
        self._headers['X-Line-Application'] = application

        j = self.get_json(self.LINE_SESSION_URL)

        session_key = j['session_key']
        message     = (chr(len(session_key)) + session_key +
                       chr(len(self.id)) + self.id +
                       chr(len(self.password)) + self.password).encode('utf-8')

        keyname, n, e = j['rsa_key'].split(",")
        pub_key       = rsa.PublicKey(int(n,16), int(e,16))
        crypto        = rsa.encrypt(message, pub_key).encode('hex')

        transport = THttpClient.THttpClient(self.LINE_HTTP_URL)
        transport.setCustomHeaders(self._headers)

        self.protocol = TCompactProtocol.TCompactProtocol(transport)
        self.client   = LineThrift.Client(self.protocol)

        msg = self.client.loginWithIdentityCredentialForCertificate(
                self.id, self.password, False, self.ip,
                self.com_name, self.provider, crypto)
        
        self._headers['X-Line-Access'] = msg.verifier
        self._pinCode = msg.pinCode
