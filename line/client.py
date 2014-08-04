# -*- coding: utf-8 -*-
"""
    line.client
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re

__all__ = ['LineClient']

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class LineClient(object):
    """This class proviede you a way to communicate with LINE server.

    :param email: NAVER id or NAVER email
    :param password: LINE password
    """

    LINE_DOMAIN = "http://gd2.line.naver.jp"

    LINE_HTTP_URL    = LINE_DOMAIN + "/api/v4/TalkService.do"
    LINE_SESSION_URL = LINE_DOMAIN + "/authct/v1/keys/line"

    provider    = None
    certificate = None
    version     = "3.7.0"
    comm_name   = "carpedm20"

    _session = requests.session()
    
    def __init__(self, id, password, is_mac=True):
        """Initialize LINE instance with provided information

        :param id: `NAVER id` or `LINE e-mail`
        :param password: LINE account password
        """
        self.id = id
        self.password = password
        self.is_mac = is_mac

        pin_code = self._login()
        print pin_code

    def _login(self):
        """Login to LINE server."""
        if EMAIL_REGEX.match(id):
            self.provider = Line.Provider.LINE
        else:
            self.provider = ine.Provider.NAVER_KR

        if self.is_mac:
            os_version  = "10.9.4-MAVERICKS-x64"
            user_agent  = "DESKTOP:MAC:%s(%s)" % (os_version, version)
            application = ("DESKTOPMAC\t%(version)\tMAC\t%(os_version)"
                           %{'version': version, 'os_version': os_version})
        else:
            os_version  = "5.1.2600-XP-x64"
            user_agent  = "DESKTOP:WIN:%s(%s)" % (os_version, version)
            application = ("DESKTOPWIN\t%(version)\tWINDOWS\t%(os_version)"
                           %{'version': version, 'os_version': os_version})

        self._headers['User-Agent']         = user_agent
        self._headers['X-Line-Application'] = application

        r = self._session.get(LINE_SESSION_URL, headers=self._headers)
        j = json.loads(r.text)

        session_key = j['session_key']
        message     = (chr(len(session_key)) + session_key +
                       chr(len(self.id)) + self.id +
                       chr(len(self.password)) + self.password).encode('utf-8')

        keyname, n, e = session_key.split(",")
        pub_key       = rsa,Publickey(int(n,16), int(e,16))
        crypto        = rsa.encrypt(message, pub_key).encode('hex')

        transport = THttpClient.THttpClient(LINE_HTTP_URL)
        transport.setCustomHeaders(self._header)

        protocol = TCompactProtocol.TCompactProtocol(transport)

        client = Line.Client(protocol)
        msg    = client.loginWithIdentityCredentialForCertificate(
                    user, message, keyname, crypto, False,
                    ip, com_name, self.provider, "")

        return msg
