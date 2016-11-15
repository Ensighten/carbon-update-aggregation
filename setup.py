#!/usr/bin/env python

from setuptools import setup

exec(open('carbon_update_aggregation/version.py').read())

config = {
    'description': 'Tool to update storage aggregations on whisper files created by carbon-cache',
    'author': 'Scott Cunningham',
    'url': 'https://github.com/ensighten/carbon-update-aggregation',
    'download_url': 'https://github.com/ensighten/carbon-update-aggregation',
    'author_email': 'infra@ensighten.com',
    # Tell flake8 to ignore this line because the variable is read from carbon_update_aggregation/version.py in a hacky way
    'version': __version__,  # NOQA
    'install_requires': ['carbon>=0.9', 'whisper>=0.9'],
    'py_modules': ['lib'],
    'packages': ['carbon_update_aggregation'],
    'scripts': ['bin/carbon-update-aggregation.py'],
    'name': 'carbon_update_aggregation'
}

setup(**config)
