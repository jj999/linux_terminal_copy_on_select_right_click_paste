#!/usr/bin/env python
#Created by Jan Andrejkovic 2016, Licence: GPLv3
import Xlib
import Xlib.display
from gi.repository import Gtk, Gdk

terminal_name = "term"        #Change "term" for your terminal WM class name
sync_for_all = False          #Set to True to do copy on select for all windows

disp = Xlib.display.Display()
root = disp.screen().root

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')

def sync_clipboard(prim):
    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    if prim.wait_is_image_available():
        clip.set_image(prim.wait_for_image())
    elif prim.wait_is_text_available():
        clip.set_text(prim.wait_for_text(), -1)

def get_window():
    window = disp.get_input_focus().focus
    wmclass = window.get_wm_class()
    if wmclass is None:
        window = window.query_tree().parent
    return window

def primary_change(*args):
    prim = args[0]
    if sync_for_all:
        sync_clipboard(prim)
    else:
        window = get_window()
        window_name = window.get_wm_class()[1]
        if terminal_name in window_name:
            sync_clipboard(prim)

primary = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
primary.connect('owner-change', primary_change)
Gtk.main()
