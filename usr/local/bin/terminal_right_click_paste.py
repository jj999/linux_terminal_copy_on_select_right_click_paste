#!/usr/bin/env python
#Created by Jan Andrejkovic 2016, Licence: GPLv3

import Xlib
import Xlib.display
import signal
import time

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
    except (AttributeError, TypeError):
        window_name = None

    return window_name

def swap_keys(disp, swapF):
    if swapF == swap_keys.swappedF:
        return
    else:
        bMap=disp.get_pointer_mapping()
        if bMap[0] == 1:
            rightHandedF=True
        elif bMap[2] == 1:
            rightHandedF=False
        else:
            print ("Fatal: Keyboard mapping detection error.")
            quit()

        if rightHandedF:
            (bMap[1], bMap[2])=((2, 3), (3, 2))[swapF]
        else:
            (bMap[0], bMap[1])=((3, 2), (2, 3))[swapF]

        #print (bMap)
        disp.set_pointer_mapping(bMap)
        swap_keys.swappedF=swapF

swap_keys.swappedF = False

def sigint_handler(signum, frame):
    swap_keys(Xlib.display.Display(), False)
    print ("\nExiting...")
    quit()

def update_windows(window):
    if window.get_wm_class() != None:
        window.change_attributes(event_mask=mask)

    for win in window.query_tree().children:
        update_windows(win)

signal.signal(signal.SIGINT, sigint_handler)

time.sleep(3)

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
                        #print('New window class: '+window_name)
                        lastName = window_name
                        if terminal_name in window_name:
                            swap_keys(disp, True)
                        else:
                            swap_keys(disp, False)
                    else:
                        if terminal_name in window_name:
                            eventA = [event.type, event.mode, event.detail]
                            if eventA != [10, 0, 4]:
                                if event.type == 9 or event.type == 7:
                                    swap_keys(disp, True)
                                elif event.type == 10 or event.type == 8:
                                    swap_keys(disp, False)
                else:
                    lastName=''
                    swap_keys(disp, False)

        except Exception, e:
        #except Xlib.error.XError, e:
            #print('Exception: ')
            #print(e)
            lastName=''
            swap_keys(disp, False)

    event = disp.next_event()
