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

# GetTube package
from gettube.base import GetTubeBase
from gettube.utils.convert import convert
from gettube.misc import *

# for gettext
_ = gettext.gettext

class GetTubeCli(GetTubeBase):
    '''
    GetTube command line interface
    '''
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
        for count, fmt in enumerate(self.fmt):
            print '%d. %s' % (count + 1, fmt)
        print '-' * 79

    def reporthook(self, count, blockSize, totalSize):
        '''
        Report hook for drawing progress bar
        '''
        percentage = count * blockSize * 100 / ((totalSize / blockSize + 1) *
                (blockSize))
        sys.stdout.write('\r' + str(percentage) + '% [')
        sys.stdout.write('=' * int(percentage / 2.5) + '>')
        sys.stdout.write(' ' * (40 - int(percentage / 2.5)) + '] ')
        if percentage == 100:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def fetch(self, fmt):
        '''
        Download and convert format if needed.
        '''
        print _('Downlaoding...')
        saved_name = self.download(fmt)

        # if downloaded extension != real extention, we need to convert
        if self.fmt[fmt][1] != self.fmt[fmt][2]:
            print _('Converting to %s, this may take a while...') % fmt
            saved_name = convert(fmt, saved_name)

        print _('Saved to `') + saved_name + '\'.'

    def interactive(self, address):
        gt = GetTubeCli()

        try:
            gt.parse_url(address)
        except Exception as e:
            print e
            return
        
        gt.show()

        choice = 0
        total = len(gt.fmt)
        avail = gt.fmt.keys()
        try:
            while choice <= 0 or choice > total:
                choice = int(raw_input(_('Choose a format: ')))
        except KeyboardInterrupt, ValueError:
            raise Exception(_('Aborted.'))

        gt.fetch(avail[choice -1])
