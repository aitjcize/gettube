# GetTubeConvert.py
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

import subprocess, os
from Misc import *
_ = gettext.gettext

def ToMp3(name):
    cmdrp = [ ("'", "\\\'"), ('"', '\\\"'), ('(', '\\('), (')', '\\)') ]
    rp_name = name
    for x, y in cmdrp:
        rp_name = rp_name.replace(x, y)

    mp3_name = name.strip('mp4') + 'mp3'
    rp_mp3_name = rp_name.strip('mp4') + 'mp3'

    cmd = 'ffmpeg -i ' + rp_name + ' -ab 128k ' + rp_mp3_name

    # Remove previous mp3 prevent ffmpeg from prompting about overwriting.
    try:
        os.remove(mp3_name)
    except OSError:
        pass

    ret = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE).wait()

    if ret != 0:
        print _('error: failed to convert {0} to MP3.').format(name)
        return -1

    os.remove(name)
    return mp3_name
