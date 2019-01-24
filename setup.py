#!/usr/bin/env python3

from setuptools import setup


exec(compile(
    open('dosm/version.py', 'r').read(),
    'dosm/version.py', 'exec'
))

DESCRIPTION: str = 'Snapshot manager for DigitalOcean volumes'
LONG_DESCRIPTION: str = 'DOSM is a snapshot scheduling library for DigitalOcean volumes'
REQUIREMENTS: list = open('requirements.txt').read().split('\n')

setup(
    name='dosm',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/amicaldo/digitalocean-snapshot-manager',
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    license=__license__,
    packages=['dosm', 'dosm.confman', 'dosm.logger'],
    install_requires=REQUIREMENTS
)
