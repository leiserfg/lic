# -*- coding: utf-8 -*-
"""
lic.license
~~~~~~~~~~~~~~~~~~~~
Tools to take a license.txt and generate a License object suitable for being used. 

:copyright: (c) 2015 by Leiser Fernández Gallo.

:license: BSD, see LICENSE for more details.
"""
from datetime import date
from getpass import getuser
from os.path import basename
from os import getcwd


from toml import loads
from click import prompt

from lic.utils import boomer

replaces = {}


def replace(*names):
    def wrap(fn):
        for name in names:
            replaces[name] = boomer(fn)
        return fn
    return wrap


@replace('year', 'yyyy')
def year():
    return prompt('Year', default=date.today().year, type=int)


@replace('fullname', 'owner', 'author')
def owner():
    return prompt('Autor or Owner name', default=getuser())


@replace('project')
def project():
    return prompt('Project Name', default=basename(getcwd()))


class License(object):

    """Take a licence.txt and buld a License instance"""

    def __init__(self, title, nick, category, source,
                 required, permitted, forbidden, body):
        self.title = title
        self.nick = nick or ''
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

        self._body = self.body.format(**replaces)

        return self._body

    def __repr__(self):
        return u'<License: %s(%s)>' % (self.title, self.nick)
