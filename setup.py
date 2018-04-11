#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import sys
sys.path.append('./tests')

setup(
	name= 'imageshuffle', # Application name:
	version= '0.2.1', # Version number

	author= 'Masayuki Tanaka', # Author name
	author_email= 'mastnk@gmail.com', # Author mail	

	url='https://github.com/mastnk/imageshuffle', # Details
	description='Image shffule library for python.', # short description
	long_description='Image shffule library for python.', # long description
	install_requires=[ # Dependent packages (distributions)
		'Pillow', 'numpy'
	],
	
	include_package_data=False, # Include additional files into the package
	packages=find_packages(),

	test_suite = 'tests',

	classifiers=[
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT',
    ]
)

# uninstall
# % python setup.py install --record installed_files
# % cat installed_files | xargs rm -rf
# % rm installed_files

