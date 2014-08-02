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

    __pinCode__ = None
    __verifier__ = None
    __provider__ = None
    __certificate__ = None

    def __init__(self, email, password):
        if EMAIL_REGEX.match(email):
            self.__provider__ = "LINE"
        else:
            self.__provider__ = "NAVER_KR"
        self.identifier = email
        self.password = password

    def _login(self):
        """Login to LINE server."""
