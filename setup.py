#!/usr/bin/env python
# coding: utf-8

import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
	name='sofart',
	version='0.0.3',
	description='Quick and dirty python embedded and non-relationnal database',
	long_description=open('README.rst').read(), 
	license=open("LICENSE").read(),
	author="Geoffrey Lehée",
	author_email="geoffrey@lehee.name",
	packages = ['sofart']
)
