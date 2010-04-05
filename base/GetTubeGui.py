# GetTubeGui.py
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

import pygtk
pygtk.require('2.0')
import gtk
import urllib, time, gettext
from GetTube import GetTube
from Misc import *
_ = gettext.gettext

class GetTubeGui(GetTube):
    def __init__(self):
        gtk.window_set_default_icon_from_file(program_logo)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(program_name)
        self.window.resize(580, 180)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_border_width(10)
        self.format = 'MP4'

        # Widgets
        self.logo = gtk.Button()
        self.logo.add(gtk.image_new_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(program_logo, 100, 100)))
        self.mainframe = gtk.Frame(_('GetTube'))
        self.address_label = gtk.Label(_('Address:'))
        self.address_text = gtk.Entry()
        self.parse_button = gtk.Button(_('Parse Address'))
        self.clear_button = gtk.Button(_('Clear'))
        self.progress_bar = gtk.ProgressBar()
        self.infoframe = gtk.Frame(_('Video Information'))
        self.infolabel = gtk.Label()
        self.info = _('Video Title: {0}\nVideo ID:    {1}\nVideo Key:   {2}')
        self.formatframe = gtk.Frame(_('Available Formats'))
        self.download_button = gtk.Button(_('Download'))
        self.download_progressbar = gtk.ProgressBar()
        self.download_progressbar.set_text(_('Ready'))
        self.fmt_but = []
        self.fmt_but.append(gtk.RadioButton(None, '3GP'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP4'))
        self.fmt_but[1].set_active(True)
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP4-1080p'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP4-720p'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'FLV'))
        self.seperator1 = gtk.HSeparator()
        self.seperator2 = gtk.HSeparator()
        self.seperator3 = gtk.HSeparator()

        # Layout
        vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        hbox = gtk.HBox(True, 0)
        hbox.pack_start(self.logo, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(self.mainframe, False, False, 0)
        hbox = gtk.HBox(False, 0)
        vbox = gtk.VBox(False, 0)
        self.mainframe.add(vbox)
        vbox.set_border_width(10)
        vbox.pack_start(hbox, True, False, 0)
        hbox.pack_start(self.address_label, False, False, 0)
        hbox.pack_start(self.address_text, True, True, 5)
        hbox.pack_start(self.progress_bar, True, True, 5)
        hbox.pack_start(self.clear_button, False, False, 5)
        hbox.pack_start(self.parse_button, False, False, 0)
        self.window.show_all()
        # following widgets is hidden
        vbox.pack_start(self.seperator1, True, True, 10)
        vbox.pack_start(self.infoframe, True, True, 0)
        hbox2 = gtk.HBox(False, 0)
        hbox2.pack_start(self.infolabel, False, False, 0)
        hbox2.set_border_width(5)
        self.infoframe.add(hbox2)
        vbox.pack_start(self.seperator2, True, True, 10)
        vbox.pack_start(self.formatframe, True, True, 0)
        hbox2 = gtk.HBox(True, 0)
        hbox2.set_border_width(5)
        for i in range(5):
            hbox2.pack_start(self.fmt_but[i], False, False, 0)
        self.formatframe.add(hbox2)
        vbox.pack_start(self.seperator3, True, True, 10)
        hbox2 = gtk.HBox(False, 0)
        hbox2.pack_start(self.download_progressbar, True, True, 0)
        hbox2.pack_start(self.download_button, False, False, 5)
        self.download_button.set_sensitive(False)
        vbox.pack_start(hbox2, True, True, 0)

        # connect
        self.fmt_but[0].connect('toggled', self.choose, '3GP')
        self.fmt_but[1].connect('toggled', self.choose, 'MP4')
        self.fmt_but[2].connect('toggled', self.choose, 'MP4-1080p')
        self.fmt_but[3].connect('toggled', self.choose, 'MP4-720p')
        self.fmt_but[4].connect('toggled', self.choose, 'FLV')
        self.clear_button.connect('clicked', self.clear_address)
        self.download_button.connect('clicked', self.download)
        self.window.connect('destroy', lambda wid: gtk.main_quit())
        self.parse_button.connect('clicked', self.parse)
        self.logo.connect('clicked', self.about_dialog)

        # main
        self.window.show()
        self.progress_bar.hide()
        self.parse_button.set_flags(gtk.CAN_DEFAULT)
        self.parse_button.grab_default()
        gtk.main()

    def clear_address(self, button):
        self.address_text.set_text('')
        self.download_progressbar.set_fraction(0)
        self.download_progressbar.set_text(_('Ready'))
        self.hide_info_block()

    def choose(self, button, format):
        if button.get_active():
            self.format = format

    def progress_bar_pulse(self):
        count = 0
        self.progress_bar.set_pulse_step(0.1)
        while count < 20:
            time.sleep(0.1)
            self.progress_bar.pulse()
            count += 1
            while gtk.events_pending():
                gtk.main_iteration()

    def hide_info_block(self):
        self.seperator1.hide()
        self.seperator2.hide()
        self.seperator3.hide()
        self.infoframe.hide()
        self.formatframe.hide()
        self.download_progressbar.hide()
        self.download_button.hide()
        self.window.resize(580, 180)

    def parse(self, button):
        address = self.address_text.get_text().strip(' ')
        if address == '':
            self.hide_info_block()
        else:
            GetTube.__init__(self, address)
            self.clear_button.set_sensitive(False)
            self.address_text.hide()
            self.progress_bar.show()
            self.progress_bar.set_text(address if len(address) <= 42
                    else address[:39] + '...')
            self.progress_bar_pulse()
            self.address_text.show()
            self.progress_bar.hide()
            self.clear_button.set_sensitive(True)
            self.info_block()
            self.download_progressbar.set_sensitive(True)
            self.download_button.set_sensitive(True)
            self.download_progressbar.set_fraction(0)
            self.download_progressbar.set_text(_('Ready'))

    def info_block(self):
        self.infolabel.set_text(self.info.format(self.title, self.id,
            self.t))
        self.mainframe.show_all()
        self.progress_bar.hide()
        total, avail = self.show()
        for i in range(5):
            if self.fmt_but[i].get_label() not in avail:
                self.fmt_but[i].hide()

    def retrieve_hook(self, count, blockSize, totalSize):
        fraction = count * blockSize / float((totalSize / blockSize + 1) *
                (blockSize))
        self.download_progressbar.set_text(str(int(fraction * 100)) + '%')
        self.download_progressbar.set_fraction(fraction)
        while gtk.events_pending():
            gtk.main_iteration()
        return True

    def download(self, button):
        self.parse_button.set_sensitive(False)
        self.download_button.set_sensitive(False)
        self.clear_button.set_sensitive(False)
        address = self.url
        if self.format != 'FLV':
            address += '&fmt=' + str(self.fmt[self.format][0])
        name = self.outfile + '.' + self.fmt[self.format][1]
        urllib.urlcleanup()
        urllib.urlretrieve(address, name, reporthook = self.retrieve_hook)
        self.download_progressbar.set_text(_('Finished'))
        self.parse_button.set_sensitive(True)
        self.download_button.set_sensitive(True)
        self.clear_button.set_sensitive(True)

    def about_dialog(self, button):
        about = gtk.AboutDialog()
        about.set_name(program_name)
        about.set_version(program_version)
        about.set_comments(_('Download YouTube video easily.'))
        about.set_license('''
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
        ''')
        about.set_copyright(_('Copyright 2010 Wei-Ning Huang (AZ)'))
        about.set_website('http://github.com/Aitjcize/gettube')
        about.set_authors(['Wei-Ning Huang (AZ <aitjcize@gmail.com>'])
        about.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(program_logo,
            128, 128))
        about.connect('response', lambda x, y, z: about.destroy(), True)
        about.show_all()
