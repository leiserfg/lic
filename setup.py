# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from lic import __version__



setup(
    name='lic',
    version=__version__,
    author='Leiser Fernández Gallo',
    author_email='leiserfg@gmail.com',
    include_package_data = True,
    packages=find_packages(),
    description='A tool to help choosing licenses',
    url='github.com',   
    #long_description=open('README.rst').read(),
    license='BSD License',
    entry_points = {
        'console_scripts': ['lic = lic.cli:cli'],
    },
    install_requires=[
        'toml',
        'click',
        'fuzzywuzzy',
        'python-Levenshtein', # for making fuzzywuzzy 4x-10x faster 
        ]
)