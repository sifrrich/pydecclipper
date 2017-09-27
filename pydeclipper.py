#!/usr/bin/env python3

"""Decrypt armored messages encrypted with gpg from clipboard
"""

import gnupg
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3

import signal

__author__ = "Franz Richter-Gottfried"
__copyright__ = "Copyright 2017, Franz Richter-Gottfried"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "sifrrich@gmail.com"
__maintainer__ = "Franz Richter-Gottfried"

APPID = "pydeclipper"
ICON = gtk.STOCK_DIALOG_AUTHENTICATION

class TrayIcon:
    def __init__(self):
        self.menu = gtk.Menu()

        self.ind = AppIndicator3.Indicator.new(
            APPID, ICON, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.ind.set_menu(self.menu)

        self.make_menu()

    def on_right_click(data, event_button, event_time):
        self.menu.popup(None, None, pos, icon, event_button, event_time)

    def on_left_click(data, event_button, event_time):
        self.decrypt()

    def message(self, text):
        win = gtk.Window(icon_name=ICON, title=APPID)
        win.set_default_size(580, 600)
        win.set_position(gtk.WindowPosition.CENTER)
        win.set_keep_above(True)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(5)
        scrolled_window.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.AUTOMATIC)

        tv = gtk.TextView()

        tv.set_editable(False)
        tv.set_cursor_visible(False)
        tv.set_wrap_mode(gtk.WrapMode.WORD)

        tv.get_buffer().set_text(text)

        scrolled_window.add(tv)

        win.add(scrolled_window)
        win.show_all()

    # Actually strips the end armor marker, but this is ok for gnupg
    def decrypt(self, data=None):
        clipboard = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD).wait_for_text()

        start = clipboard.find("-----BEGIN PGP MESSAGE-----")
        end = clipboard[start:].rfind("-----END PGP MESSAGE-----")

        clipboard = clipboard[start:end]

        if not -1 in {start, end}:
            gpg = gnupg.GPG(verbose=False, use_agent=True)
            decrypted = gpg.decrypt(clipboard)

            if decrypted.ok:
                self.message(str(decrypted))

    def close_app(self, data=None):
        gtk.main_quit()

    def make_menu(self):
        decrypt_item = gtk.MenuItem("Decrypt")
        close_item = gtk.MenuItem("Close")

        #Append the menu items
        self.menu.append(decrypt_item)
        self.menu.append(close_item)

        #add callbacks
        decrypt_item.connect("activate", self.decrypt)
        close_item.connect("activate", self.close_app)

        self.menu.show_all()

def main():
    TrayIcon()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    gtk.main()

if __name__ == "__main__":
    main()

#  vim: set ts=8 sw=4 ft=python tw=80 nolinebreak et nospell spelllang=en :
