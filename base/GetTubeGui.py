#-*- coding: utf-8 -*-
#
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
import locale, os.path, sys, time, gettext
from GetTubeBase import GetTubeBase
from GetTubeConvert import ToMp3
from GetTubeMisc import *
_ = gettext.gettext

class GetTubeGui(GetTubeBase):
    def __init__(self):
        gtk.window_set_default_icon_from_file(program_logo)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(program_name)
        self.window.resize(620, 180)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_border_width(10)
        self.format = 'MP4'
        self.out_prefix = os.path.expanduser('~/').rstrip('/')

        # Widgets
        self.banner = gtk.image_new_from_pixbuf(
                gtk.gdk.pixbuf_new_from_file_at_size(program_banner, 600, 100))
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
        self.abort_download_button = gtk.Button(_('Abort'))
        self.download_button = gtk.Button(_('Download to ...'))
        self.download_progressbar = gtk.ProgressBar()
        self.download_progressbar.set_text(_('Ready'))
        self.fmt_but = []
        self.fmt_but.append(gtk.RadioButton(None, '3GP'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP4'))
        self.fmt_but[1].set_active(True)
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP4-1080p'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP4-720p'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'FLV'))
        self.fmt_but.append(gtk.RadioButton(self.fmt_but[0], 'MP3'))
        self.version_label = gtk.Label(_('Version %s') % program_version)
        self.about_button = gtk.Button(_('About this program'))

        # Layout
        Ovbox = gtk.VBox(False, 0)
        self.window.add(Ovbox)
        Ovbox.pack_start(self.banner, False, False, 0)
        Ovbox.pack_start(self.mainframe, False, False, 5)
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
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 10)
        vbox.pack_start(self.infoframe, True, True, 0)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(self.infolabel, False, False, 0)
        hbox.set_border_width(5)
        self.infoframe.add(hbox)
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 10)
        vbox.pack_start(self.formatframe, True, True, 0)
        hbox = gtk.HBox(True, 0)
        hbox.set_border_width(5)
        for i in range(len(self.fmt_but)):
            hbox.pack_start(self.fmt_but[i], False, False, 0)
        self.formatframe.add(hbox)
        separator = gtk.HSeparator()
        vbox.pack_start(separator, True, True, 10)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(self.download_progressbar, True, True, 0)
        hbox.pack_start(self.abort_download_button, False, False, 5)
        hbox.pack_start(self.download_button, False, False, 5)
        self.abort_download_button.set_sensitive(False)
        self.download_button.set_sensitive(False)
        vbox.pack_start(hbox, True, True, 5)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(self.version_label, False, False, 0)
        hbox.pack_end(self.about_button, False, False, 0)
        Ovbox.pack_start(hbox, False, False, 0)
        self.clear_info_block(None)

        # Connect
        self.fmt_but[0].connect('toggled', self.choose, '3GP')
        self.fmt_but[1].connect('toggled', self.choose, 'MP4')
        self.fmt_but[2].connect('toggled', self.choose, 'MP4-1080p')
        self.fmt_but[3].connect('toggled', self.choose, 'MP4-720p')
        self.fmt_but[4].connect('toggled', self.choose, 'FLV')
        self.fmt_but[5].connect('toggled', self.choose, 'MP3')
        self.clear_button.connect('clicked', self.clear_info_block)
        self.abort_download_button.connect('clicked', self.abort)
        self.download_button.connect('clicked', self.file_choose_dialog)
        self.window.connect('delete_event', self.close_dialog)
        self.parse_button.connect('clicked', self.parse)
        self.about_button.connect('clicked', self.about_dialog)

        # Main
        self.window.show_all()
        self.progress_bar.hide()
        gtk.main()

    def choose(self, button, format):
        '''
        Callback for selecting format
        '''
        if button.get_active():
            self.format = format

    def progress_bar_pulse(self):
        '''
        Progress bar pulse
        '''
        count = 0
        self.progress_bar.set_pulse_step(0.1)
        while count < 10:
            time.sleep(0.1)
            self.progress_bar.pulse()
            count += 1
            while gtk.events_pending():
                gtk.main_iteration()

    def update_info_block(self):
        '''
        Update the information block including infoframe, formatframe
        '''
        self.infolabel.set_text(self.info.format(self.title, self.id,
            self.t))
        self.mainframe.show_all()
        self.progress_bar.hide()
        total, avail = self.show()
        for i in range(len(self.fmt_but)):
            if self.fmt_but[i].get_label() not in avail:
                self.fmt_but[i].hide()

    def clear_info_block(self, button):
        '''
        Clear the information block including infoframe, formatframe
        '''
        self.window.resize(620, 180)
        self.infolabel.set_text(self.info.format('N/A', 'N/A', 'N/A'))
        self.address_text.set_text('')
        self.download_progressbar.set_fraction(0)
        self.download_progressbar.set_text(_('Ready'))
        self.formatframe.show_all()
        for i in range(len(self.fmt_but)):
            self.fmt_but[i].set_sensitive(False)

    def parse(self, button):
        '''
        Parse URL by passing address to the base class constructor
        '''
        address = self.address_text.get_text().strip(' ')
        if address == '':
            self.clear_info_block(None)
        else:
            try:
                GetTubeBase.__init__(self, address)
            except Exception:
                self.error_dialog(_('Invalid URL, please reenter.'))
                self.retries = 5
                return

            self.clear_button.set_sensitive(False)
            self.address_text.hide()
            self.progress_bar.show()
            self.progress_bar.set_text(address if len(address) <= 42
                    else address[:40] + '...')
            self.progress_bar_pulse()
            self.address_text.show()
            self.progress_bar.hide()
            self.clear_button.set_sensitive(True)
            for i in range(len(self.fmt_but)):
                self.fmt_but[i].set_sensitive(True)
            self.update_info_block()
            self.download_progressbar.set_sensitive(True)
            self.download_button.set_sensitive(True)
            self.download_progressbar.set_fraction(0)
            self.download_progressbar.set_text(_('Ready'))

    def retrieve_hook(self, count, blockSize, totalSize):
        '''
        Overriding the base class retrieve_hook for displaying graphical
        progress bar
        '''
        fraction = count * blockSize / float((totalSize / blockSize + 1) *
                (blockSize))
        self.download_progressbar.set_text(str(int(fraction * 100)) + '%')
        self.download_progressbar.set_fraction(fraction)
        while gtk.events_pending():
            gtk.main_iteration()

    def download(self, name):
        '''
        Overriding the base class download to provide graphical interaction.
        '''
        self.parse_button.set_sensitive(False)
        self.abort_download_button.set_sensitive(True)
        self.download_button.set_sensitive(False)
        self.clear_button.set_sensitive(False)
        self.formatframe.set_sensitive(False)
        address = self.url
        if self.format != 'FLV':
            address += '&fmt=' + str(self.fmt[self.format][0])
        encoding = locale.getdefaultlocale()[1]
        if name[-4:] != '.' + self.fmt[self.format][1]:
            name = name + '.' + self.fmt[self.format][1]
        name = name.encode(encoding)
        self.retrieve(address, name, self.retrieve_hook)

        if self.abort_download:
            self.abort_download = False
            self.download_progressbar.set_fraction(1)
            self.download_progressbar.set_text(_('Aborted'))
        else:
            self.download_progressbar.set_text(_('Done'))
            self.abort_download_button.set_sensitive(False)

            # Conversion
            if self.format == 'MP3':
                self.download_progressbar.set_text(_('Converting to MP3, this '
                    'may take a while...'))

                # update GUI
                while gtk.events_pending():
                    gtk.main_iteration()

                name = ToMp3(name, True)

                if name == -1:
                    self.error_dialog(_('Some error occured during the '
                        'conversion, please try again.'))
                    self.download_progressbar.set_text(_('Failed'))
                else:
                    self.download_progressbar.set_text(_('Done'))

        self.parse_button.set_sensitive(True)
        self.abort_download_button.set_sensitive(False)
        self.download_button.set_sensitive(True)
        self.clear_button.set_sensitive(True)
        self.formatframe.set_sensitive(True)

    def file_choose_dialog(self, button):
        '''
        file choose dialog
        '''
        file_dialog = gtk.FileChooserDialog(_('Choose a location'),
                self.window, gtk.FILE_CHOOSER_ACTION_SAVE,
                (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL,
                    gtk.RESPONSE_CANCEL), None)

        file_dialog.set_current_folder(self.out_prefix)
        file_dialog.set_current_name(self.outfile);
        filter = gtk.FileFilter()
        filter.add_pattern('*.' + self.fmt[self.format][1])
        file_dialog.set_filter(filter)

        response = file_dialog.run()
        if response == gtk.RESPONSE_OK:
            fn = file_dialog.get_filename()
            file_dialog.destroy()
            self.download(fn)
        else:
            file_dialog.destroy()

    def error_dialog(self, message):
        '''
        Error dialog for convenience
        '''
        dialog = gtk.MessageDialog(self.window, 0, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_OK, '\n' + message)
        dialog.run()
        dialog.destroy()

    def close_dialog(self, widget, event):
        '''
        Callback for 'delete_event' to prevent from interrupting download
        process
        '''
        # if not downloading, quit quietly
        if self.download_progressbar.get_fraction() == 0 or\
                self.download_progressbar.get_fraction() == 1:
            gtk.main_quit()
            return False

        dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
                gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,
                _('Download in progress'))
        dialog.format_secondary_text(_('Do you want to quit?'))
        ret = dialog.run()
        dialog.destroy()
        if ret == gtk.RESPONSE_YES:
            self.abort_download = True
            gtk.main_quit()
            return False
        return True

    def about_dialog(self, button):
        '''
        About this program
        '''
        about = gtk.AboutDialog()
        about.set_position(gtk.WIN_POS_CENTER)
        about.set_name(program_name)
        about.set_version(program_version)
        about.set_comments(_('Download YouTube video Easily\n With formats:\nMP3, MP4, FLV and MP4-HD'))
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
        about.set_website_label('GetTube at GitHub')
        about.set_authors(['Wei-Ning Huang (AZ) <aitjcize@gmail.com>'])
        about.set_translator_credits('Wei-Ning Huang (AZ) '
                '<aitjcize@gmail.com>')
        about.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(program_logo,
            96, 96))
        about.connect('response', lambda x, y, z: about.destroy(), True)
        about.show_all()
