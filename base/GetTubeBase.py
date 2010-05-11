#-*- coding: utf-8 -*-
#
# GetTubeBase.py
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

import os, sys, re, urllib2, platform
from GetTubeConvert import ToMp3
from GetTubeMisc import *
_ = gettext.gettext

class GetTubeBase:
    # static variable for counting retries
    retries = 5
    def __init__(self, addr):
        '''
        Initialize and parse video information
        '''
        # Title replacement strings
        xmlrp = [ (' ', '_'), ('/', ''), ('&quot;', '"'), ('&lt;', '<'),
                ('&gt;', '>') ]

        # Windows does not allow `"' to appear in filename
        if platform.system() == 'Windows':
            xmlrp[1] = ('&quot;', '\'')

        # Valitdate URL
        if addr[0:31] != 'http://www.youtube.com/watch?v=':
            raise Exception(_('error: invalid URL.'))

        data = str(urllib2.urlopen(addr).read())
        
        # abort_download flag
        self.abort_download = False

        try:
            # address
            self.address = addr
            # id
            self.id = re.search('v=([^&]*)', addr).group(1)
            # t
            self.t = re.search('&t=(.{46})', data).group(1)
            # title
            self.title = re.search('content="([^"]*)"', data).group(1)
        except AttributeError:
            if self.retries > 0:
                print _('error: some error occured during parsing URL, '
                        'retris = '), self.retries
                self.retries -= 1
                GetTubeBase.__init__(self, addr)
            raise Exception(_('error: invalid URL.'))

        # outfile
        self.outfile = self.title
        for x, y in xmlrp:
            self.outfile = self.outfile.replace(x, y)
        # url
        self.url = 'http://www.youtube.com/get_video?video_id=' + self.id +\
                '&t=' + self.t
        # fmt
        self.fmt = {'FLV': (0, 'flv'), '3GP': (17, '3gp'), 'MP4': (18, 'mp4'),
                'MP4-720p': (22, 'mp4'), 'MP4-1080p': (37, 'mp4'),
                'MP3': (18, 'mp4')}
        # disable HD if not found
        if '22%2F2000000%' not in data:
            self.fmt['MP4-720p'] = (-1, 'mp4')
        if '37%2F4000000%2F9%2F0%2F115' not in data:
            self.fmt['MP4-1080p'] = (-1, 'mp4')

    def show(self):
        '''
        Show and return video information
        '''
        print '-' * 79
        print _('Title:'), self.title
        print _('Video ID:'), self.id
        print _('Video key:'), self.t
        print '-' * 79
        print _('Available format:')
        count = 0
        avail = []
        for key, value in self.fmt.items():
            if value[0] != -1:
                print '{0}. {1}'.format(count + 1, key)
                avail.append(key)
                count += 1
        print '-' * 79
        return count, avail

    def retrieve_hook(self, count, blockSize, totalSize):
        '''
        Retrieve for drawing progress bar
        '''
        percentage = count * blockSize * 100 / ((totalSize / blockSize + 1) *
                (blockSize))
        sys.stdout.write('\r' + str(percentage) + '% [')
        sys.stdout.write('=' * int(percentage / 2.5) + '>')
        sys.stdout.write(' ' * int(40 - percentage / 2.5) + '] ')
        if percentage == 100:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def download(self, fmt):
        '''
        Start download
        '''
        if fmt not in self.fmt or self.fmt[fmt][0] == -1:
            print _('{0} is not available for this video!').format(fmt)
            sys.exit(1)
        url = self.url + '&fmt=' + str(self.fmt[fmt][0])
        name = self.outfile + '.' + self.fmt[fmt][1]
        print _('Downloading...')
        self.retrieve(url, name, self.retrieve_hook)

        # Conversion
        if fmt == 'MP3':
            print _('Converting to MP3, this may take a while...')
            name = ToMp3(name)
            if name == -1:
                print _('error: some error occured during the conversion, '
                        'please try again.')
                sys.exit(1)

        print _('Saved to `') + name + '\'.'

    def abort(self, button):
        '''
        Set abort flag
        '''
        self.abort_download = True

    def retrieve(self, url, name, hook):
        '''
        retrieve implement with urllib2
        '''
        count = 0
        blockSize = 4096
        f = open(name, 'wb')

        urlobj = urllib2.urlopen(url)
        totalSize = int(urlobj.info()['content-length'])

        try:
            while not self.abort_download:
                data = urlobj.read(blockSize)
                count += 1
                if not data:
                    break
                f.write(data)
                hook(count, blockSize, totalSize)
        except KeyboardInterrupt:
            f.close()
            os.remove(name)
            print _('\nAborted.')
            sys.exit(1)

        f.close()
        if self.abort_download:
            try:
                os.remove(name)
            except OSError:
                pass
