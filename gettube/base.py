#-*- coding: utf-8 -*-
#
# base.py
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

import os
import re
import urllib2

# GetTube package
from gettube.misc import *

# for gettext
_ = gettext.gettext

class GetTubeBase:
    '''
    Base for the GetTube class hierarchy.
    GetTube -- GetTubeCli
            \- GetTubeGui
    '''

    # static variable for counting retries
    retries = 5

    def __init__(self):
        # Things need to be done are in parse_url
        pass

    def parse_url(self, addr):
        '''
        Parse video information.
        '''

        # Title replacement pairs
        xmlrp = [ (' ', '_'), ('/', ''), ('&quot;', '"'), ('&lt;', '<'),
                ('&gt;', '>') ]

        # Windows does not allow `"' to appear in filename
        if running_os == 'Windows':
            xmlrp[2] = ('&quot;', '\'')

        # Reset abort_download flag
        self.abort_download = False
        self.address = addr

        # Valitdate URL
        if self.address[0:31] != 'http://www.youtube.com/watch?v=':
            raise RuntimeError(_('Invalid URL.'))

        data = str(urllib2.urlopen(addr).read())

        try:
            # id
            self.id = re.search('v=([^&]*)', addr).group(1)
            # t
            self.t = re.search('&t=(.{46})', data).group(1)
            # title
            self.title = re.search('content="([^"]*)"', data).group(1)
        except AttributeError:
            print _('Error while parsing URL, retries = %d') % self.retries
            self.retries -= 1
            if not self.retries:
                raise RuntimeError(_('Invalid URL.'))
            else:
                self.parse_url(self.address)

        # Replace title xml markings
        for x, y in xmlrp:
            self.title = self.title.replace(x, y)
        self.outname = self.title

        # url
        self.download_url = 'http://www.youtube.com/get_video?video_id=%s'\
                '&eurl=&el=&ps=&asv=&t=%s' % (self.id, self.t)

        # List of supported formats
        # self.fmt[FMT] = [download_type, downloaded_extension, real_extension]
        self.fmt = {}
        self.fmt['FLV'] = [0, 'flv', 'flv']
        self.fmt['3GP'] = [17, '3gp', '3gp']
        self.fmt['MP4'] = [18, 'mp4', 'mp4']
        self.fmt['MP4-720p'] = [22, 'mp4', 'mp4']
        self.fmt['MP4-1080p'] = [37, 'mp4', 'mp4']
        self.fmt['MP3'] = [18, 'mp4', 'mp3']

        # disable HD if not found
        if '22%2F1280x720' not in data:
            self.fmt.pop('MP4-720p')
        if '37%2F1920x1080' not in data:
            self.fmt.pop('MP4-1080p')

    def reporthook(self, count, blockSize, totalSize):
        '''
        Report hook for drawing progress bar
        '''
        pass

    def download(self, fmt, outname = None):
        '''
        Start download
        '''
        if not outname:
            outname = self.outname[:]

        url = self.download_url
        if fmt != 'FLV':
            url += '&fmt=' + str(self.fmt[fmt][0])
        
        if outname[-4:] != '.' + self.fmt[fmt][1]:
            outname += '.' + self.fmt[fmt][1]

        try:
            self.url_retrieve(url, outname, self.reporthook)
        except KeyboardInterrupt:
            try:
                os.remove(outname)
            except OSError:
                pass
            raise Exception(_('Aborted.'))

        return outname

    def abort(self, button):
        '''
        Set abort flag
        '''
        self.abort_download = True

    def url_retrieve(self, url, save_name, reporthook):
        '''
        Like the one in urllib. Unlike urllib.retrieve url_retrieve
        can be interrupted. KeyboardInterrupt exception is rasied when
        interrupted.
        '''
        count = 0
        blockSize = 1024 * 8
        f = open(save_name, 'wb')

        urlobj = urllib2.urlopen(url)

        totalSize = int(urlobj.info()['content-length'])

        try:
            while not self.abort_download:
                data = urlobj.read(blockSize)
                count += 1
                if not data:
                    break
                f.write(data)
                reporthook(count, blockSize, totalSize)
        except KeyboardInterrupt:
            f.close()
            self.abort_download = True

        if self.abort_download:
            raise KeyboardInterrupt

        del urlobj
        f.close()
