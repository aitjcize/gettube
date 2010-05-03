#-*- coding: utf-8 -*-
#
# GetTubeMisc.py
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

from os.path import exists, abspath, dirname
import sys
import gettext, platform

# Program Information
program_name = 'GetTube'
program_name_lower_case = 'gettube'
program_version = '0.6.8'

program_logo = '/usr/share/pixmaps/gettube.png'
program_banner = '/usr/share/pixmaps/gettubebanner.png'

# If lanuch from source directory
if not exists(program_logo):
    prefix = dirname(abspath(sys.argv[0]))
    program_logo = prefix + '/../images/gettube.png'
    program_banner = prefix + '/../images/gettubebanner.png'

if platform.system() == 'Windows':
    program_logo = 'gettube.png'

# For gettext
gettext.bindtextdomain(program_name_lower_case)
gettext.textdomain(program_name_lower_case)