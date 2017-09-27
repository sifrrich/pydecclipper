#!/usr/bin/env python3

import gnupg
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

import signal

APPID = "pydeclipper"
ICON = gtk.STOCK_DIALOG_AUTHENTICATION

class TrayIcon:
    def __init__(self):
        self.menu = gtk.Menu()

        APPIND_SUPPORT = True
        try:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3
        except:
            APPIND_SUPPORT = False


        if APPIND_SUPPORT == True:
            self.ind = AppIndicator3.Indicator.new(
                APPID, ICON, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.ind.set_menu(self.menu)
        else:
            self.ind = gtk.StatusIcon()
            self.ind.new_from_icon_name("process-stop")

            self.ind.connect('popup-menu', self.on_right_click)
            self.ind.connect('activate', self.on_left_click)

            self.ind.set_visible(True)

        self.make_menu()

    def on_right_click(data, event_button, event_time):
        print("right click")
        self.menu.popup(None, None, pos, icon, event_button, event_time)

    def on_left_click(data, event_button, event_time):
        print("left click")
        self.decrypt()

    def message(self, text):
        msg = gtk.MessageDialog(None, 0, gtk.MessageType.INFO,
                gtk.ButtonsType.OK, text, title=APPID,transient_for=None)
        msg.run()
        msg.destroy()

    def decrypt(self, data=None):
        clipboard = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD).wait_for_text()

        start = clipboard.find("-----BEGIN PGP MESSAGE-----")
        end = clipboard.find("-----END PGP MESSAGE-----")

        if not -1 in {start, end}:
            gpg = gnupg.GPG(verbose=False, use_agent=True)
            decrypted = gpg.decrypt(clipboard)
            self.message(decrypted)

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
