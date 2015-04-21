# -*- coding: utf-8 -*-
"""
lic.license
~~~~~~~~~~~~~~~~~~~~
Tools to take a license.txt and generate a License object suitable for being used. 

:copyright: (c) 2015 by Leiser Fernández Gallo.

:license: BSD, see LICENSE for more details.
"""
import re

from datetime import date
from getpass import getuser
from os.path import dirname
from os import getcwd


from toml import loads
from click import prompt


_replaces = {}


def replace(*names):
    def wrap(fn):
        for name in names:
            _replaces[name] = fn
        return fn
    return wrap


@replace('year')
def year():
    return prompt('Year', default=date.today().year, type=int)


@replace('ower', 'author')
def owner():
    return prompt('Autor or Owner name', default=getuser())


@replace('project')
def owner():
    return prompt('Project Name', default=dirname(getcwd()))




class License(object):

    """Take a licence.txt and buld a License instance"""

    _re_replaceable = re.compile('{([^}]+)}')

    def __init__(self, title, nick, category, source,
                 required, permitted, forbidden, body):
        self.title = title
        self.nick = nick
        self.category = category
        self.source = source
        self.required = required
        self.permitted = permitted
        self.forbidden = forbidden
        self.body = body

    @staticmethod
    def load(file):
        meta, body = file.read().split('---')

        meta = loads(meta)
        license = License(meta.get('title'),
                          meta.get('nickname', ''),
                          meta.get('category'),
                          meta.get('source', ''),
                          meta.get('required', []),
                          meta.get('permitted', []),
                          meta.get('forbidden', []),
                          body
                          )
        return license

    @property
    def filledbody(self):
        if hasattr(self, '_body'):
            return self._body

        body = self.body
        
        replaceables = set(self._re_replaceable.findall(body))
        replaces = {}

        for r in replaceables:
            if r in _replaces:
                replaces[r] = _replaces[r]()
            else:
                replaces[r] = prompt(r)

        print replaces
        self._body = body.format(replaces)

        return self._body


