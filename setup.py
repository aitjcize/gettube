#!/usr/bin/env python

from distutils.core import setup
from DistUtilsExtra.command import *

_data_files = [
	('share/applications', ['misc/gettube.desktop']),
	('share/pixmaps', ['images/gettube.png']),
	('share/gettube', ['images/gettube.png']),
	('share/gettube', ['images/gettubebanner.png']),
	('share/man/man1', ['misc/gettube.1'])
	]

files = ["__init__.py",
         "base.py",
         "gui.py",
	 "cli.py",
	 "misc.py",
	 "utils/__init__.py",
	 "utils/convert.py",
	]

setup(
	name = 'gettube',
	version = '0.6.9',
	description = 'Download YouTube Videos, Fast and Easy!',
	author = 'Wei-Ning Huang (AZ)',
	author_email = 'aitjcize@gmail.com',
        url = 'http://berelent.blogspot.com/p/gettube-download-youtube-video-fast-and.html',
	license = 'GPL',
    	packages = ['gettube'],
	package_data = {'gettube' : files },
	scripts = ['bin/gettube'],
	data_files = _data_files,
        cmdclass = { "build": build_extra.build_extra,
                     "build_i18n": build_i18n.build_i18n }
)