#!/usr/bin/env python

from distutils.core import setup
from DistUtilsExtra.command import *

_data_files = [
	('share/applications', ['misc/gettube.desktop']),
	('share/pixmaps', ['images/gettube.png']),
	('share/gettube/images', ['images/gettube.png']),
	('share/gettube/images', ['images/gettubebanner.png']),
	('share/man/man1', ['misc/gettube.1'])
	]

files = ["doc/README",
         "doc/AUTHORS",
         "doc/COPYING",
         "doc/Changlog"]

setup(
	name = 'gettube',
	version = '0.7.1',
	description = 'Download YouTube Videos, Fast and Easy!',
	author = 'Wei-Ning Huang (AZ)',
	author_email = 'aitjcize@gmail.com',
        url = 'http://berelent.blogspot.com/p/gettube-download-youtube-video-fast-and.html',
	license = 'GPL',
    	packages = ['gettube', 'gettube.utils'],
	package_data = {'gettube' : files },
	scripts = ['bin/gettube'],
	data_files = _data_files,
        cmdclass = { "build": build_extra.build_extra,
                     "build_i18n": build_i18n.build_i18n }
)
