__version__ = 0.1

from codecs import open
from license import License

f = open('_licenses/agpl-3.0.txt', encoding='utf-8')
l = License.load(f)

print l.filledbody

