from os.path import join, abspath, dirname
from glob import glob
from codecs import open

from click import get_app_dir

from fuzzywuzzy.process import extractOne, extractBests

from lic.license import License

_here = dirname(abspath(__file__))
_user_licenses = get_app_dir('lic')

licenses_paths = [join(_here, '_licenses')]

class NotFound(Exception):
    pass

class Manager(object):
    def __init__(self):
        self.licenses = []
        for p in licenses_paths:
            for lic in glob(join(p, '*.lic')):
                f = open(lic, encoding='utf-8')
                self.licenses.append(License.load(f))

    def find_one(self, query, by_nick=False):
        field = 'nick' if by_nick else 'title'
        choices = {getattr(lic, field): lic for lic in self.licenses}
        field_value, _ = extractOne(query,  choices.iterkeys())

        if field_value:
            return choices[field_value]
        else:
            raise NotFound('Nothing match with %s' % query)

    def list(self, query=None, by_nick=False):
        if query is None:
            return self.licenses

        field = 'nick' if by_nick else 'title'
        choices = {getattr(lic, field): lic for lic in self.licenses}
        print choices
        field_values = extractBests(query, choices.iterkeys())

        lics = [choices[v] for v, _ in field_values]
        return lics

