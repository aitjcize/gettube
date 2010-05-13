#-*- coding: utf-8 -*-
#
# convert.py
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

import subprocess, os, time, gtk
from gettube.misc import *
_ = gettext.gettext

def ToMp3(name, gui_running = False):
    '''
    Convert MP4 to MP3
    '''
    mp3_name = name.strip('mp4') + 'mp3'

    cmd = ['ffmpeg', '-i', name, '-ab', '128k', mp3_name]

    # Remove previous mp3 prevent ffmpeg from prompting about overwriting.
    try:
        os.remove(mp3_name)
    except OSError:
        pass

    sobj = subprocess.Popen(cmd)

    try:
        while str(sobj.poll()) == 'None':
            time.sleep(1)
            # Prevent GUI from idling
            while gui_running and gtk.events_pending():
                gtk.main_iteration()
    except KeyboardInterrupt:
        os.remove(mp3_name)
        print _('Aborted.')
        return -1

    if sobj.poll() != 0:
        print _('error: failed to convert {0} to MP3.').format(name)
        return -1

    return mp3_name
