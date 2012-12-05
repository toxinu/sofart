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
	version='0.2.6',
	description='Python in-memory embedded and non-relationnal database',
	long_description=open('README.rst').read(), 
	license=open("LICENSE").read(),
	author="Geoffrey Lehée",
	author_email="geoffrey@lehee.name",
	packages = ['sofart', 'sofart.serializers'],
	install_requires = ['isit'],
	classifiers=(
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
	)
)
