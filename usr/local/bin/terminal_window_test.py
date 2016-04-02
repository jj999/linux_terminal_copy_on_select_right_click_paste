#!/usr/bin/env python
#Created by Jan Andrejkovic 2016, Licence: GPLv3

from __future__ import print_function
import Xlib
import Xlib.display
import Xlib.error
import signal

terminal_name = "term"		#Change "term" for your terminal WM class name

def update_attr(event, mask):
    try:
        ec = Xlib.error.CatchError(Xlib.error.BadWindow)
        event.window.change_attributes(event_mask=mask, onerror = ec)
    except Exception:
        pass

def get_window_class_name(event):
    try:
        window_name=event.window.get_wm_class()[1]
    except Exception:
        window_name = None

    return window_name

def sigint_handler(signum, frame):
    print ("\nExiting...")
    quit()

def update_windows(window):
    if window.get_wm_class() != None:
        window.change_attributes(event_mask=mask)

    for win in window.query_tree().children:
        update_windows(win)

signal.signal(signal.SIGINT, sigint_handler)

disp = Xlib.display.Display()
root = disp.screen().root
mask = Xlib.X.FocusChangeMask | Xlib.X.EnterWindowMask | Xlib.X.LeaveWindowMask | Xlib.X.SubstructureNotifyMask

root.change_attributes(event_mask=mask)
update_windows(root)

event = type('',(),{'type':0, 'mode':0, 'detail':0})()    #event init

lastName = ''
excludeA=[16, 17, 18, 22, 33, 34]

while True:
    if not event.type in excludeA:
        try:
            update_attr(event, mask)
            if hasattr(event, 'detail') and event.detail != Xlib.X.NotifyInferior:
                window_name = get_window_class_name(event)
                if window_name != None:
                    if lastName != window_name:
                        print('New window class: '+window_name,end="")
                        lastName = window_name
                        if terminal_name in window_name:
                            print ("  (is terminal)")
                        else:
                            print ("  (isn't terminal)")
                else:
                    lastName=''

        except Exception, e:
        #except Xlib.error.XError, e:
            #print('Exception: ')
            #print(e)
            lastName=''

    event = disp.next_event()
