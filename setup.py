#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('./requirements.txt', 'r') as stream:
    reqs = stream.readlines()

config = {
    'description': 'sup',
    'author': 'Dan Cohen',
    'url': 'https://github.com/danie1cohen/sup.git',
    'download_url': 'https://github.com/daine1cohen/sup.git',
    'author_email': 'dcohen@usccreditunion.org',
    'version': '0.0.6',
    'install_requires': reqs,
    'packages': ['sup'],
    'scripts': ['bin/sup', ],
    'name': 'sup'
}

setup(**config)
