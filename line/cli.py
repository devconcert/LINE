#-*- coding: utf-8 -*-
"""
    line.cli
    ~~~~~~~~

    LINE command line interface

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""

import sys
import os

class LineCLI(object):
    """LINE command line interface object.

    :param client: LineClient instance
    """
    def __init__(self, client):
        self.client = client

        print self.__dict__.items()
        
