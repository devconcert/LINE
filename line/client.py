# -*- coding: utf-8 -*-
"""
    line.client
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals

__all__ = ['LineClient']

class LineClient(object):
    """This class proviede you a way to communicate with LINE server.

    :param email:
    """

    __certificate__ = None

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def _login(self):
        """Login to LINE server."""
