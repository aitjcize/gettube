#-*- coding: utf-8 -*-
#
# misc.py
#
# Copyright (C) 2010 -  Wei-Ning Huang (AZ) <aitjcize@gmail.com>
# All Rights reserved.
# 
# This Program is part of GetTube.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from os.path import abspath, dirname
import sys
import gettext, platform

# Installation information
LIB_PATH = '/usr/lib/gettube'
SHARE_PATH = '/usr/share/gettube'

# Operating system
running_os = platform.system()

# Program Information
program_name = 'GetTube'
program_version = '0.7.2'

program_logo = SHARE_PATH + '/images/gettube.png'
program_banner = SHARE_PATH + '/images/gettubebanner.png'

# For py2exe packaging
if running_os == 'Windows':
    program_logo = 'gettube.png'
    program_banner = 'gettubebanner.png'

# If lanuch from source directory
if not sys.argv[0].startswith('/usr/bin'):
    prefix = dirname(abspath(sys.argv[0]))
    program_logo = prefix + '/../images/gettube.png'
    program_banner = prefix + '/../images/gettubebanner.png'

# For gettext
gettext.bindtextdomain(program_name.lower())
gettext.textdomain(program_name.lower())
