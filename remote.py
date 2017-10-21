#!/usr/bin/env python

"""
Name: remote.py
Version: 1.0
Description: cec remote control for emulation station and retroarch in retropie
Author: marcin.sielski@gmail.com
Homepage: https://github.com/marcin-sielski/RetroPie-Remote
Licence: GPL3

It depends on python-uinput package which contains
the library and the udev rules at
/etc/udev/rules.d/40-uinput.rules

cec-utils also needs to be installed

to run the code as a non root user
sudo addgroup uinput
sudo adduser pi uinput
"""

import subprocess
import uinput
import sys
import time
from time import sleep


def get_keymap():
    """Map supported keys to python-uinput keys"""

    keymap = {
            'left': uinput.KEY_LEFT, 'right': uinput.KEY_RIGHT,
            'up': uinput.KEY_UP, 'down': uinput.KEY_DOWN,
            'enter': uinput.KEY_ENTER, 'kp_enter': uinput.KEY_KPENTER,
            'tab': uinput.KEY_TAB, 'insert': uinput.KEY_INSERT,
            'del': uinput.KEY_DELETE, 'end': uinput.KEY_END,
            'home': uinput.KEY_HOME, 'rshift': uinput.KEY_RIGHTSHIFT,
            'shift': uinput.KEY_LEFTSHIFT, 'rctrl': uinput.KEY_RIGHTCTRL,
            'ctrl': uinput.KEY_LEFTCTRL, 'ralt': uinput.KEY_RIGHTALT,
            'alt': uinput.KEY_LEFTALT, 'space': uinput.KEY_SPACE,
            'escape': uinput.KEY_ESC, 'kp_minus': uinput.KEY_KPMINUS,
            'kp_plus': uinput.KEY_KPPLUS, 'f1': uinput.KEY_F1,
            'f2': uinput.KEY_F2, 'f3': uinput.KEY_F3,
            'f4': uinput.KEY_F4, 'f5': uinput.KEY_F5,
            'f6': uinput.KEY_F6, 'f7': uinput.KEY_F7,
            'f8': uinput.KEY_F8, 'f9': uinput.KEY_F9,
            'f10': uinput.KEY_F10, 'f11': uinput.KEY_F11,
            'f12': uinput.KEY_F12, 'num1': uinput.KEY_1,
            'num2': uinput.KEY_2, 'num3': uinput.KEY_3,
            'num4': uinput.KEY_4, 'num5': uinput.KEY_5,
            'num6': uinput.KEY_6, 'num7': uinput.KEY_7,
            'num8': uinput.KEY_8, 'num9': uinput.KEY_9,
            'num0': uinput.KEY_0, 'pageup': uinput.KEY_PAGEUP,
            'pagedown': uinput.KEY_PAGEDOWN, 'keypad1': uinput.KEY_KP1,
            'keypad2': uinput.KEY_KP2, 'keypad3': uinput.KEY_KP3,
            'keypad4': uinput.KEY_KP4, 'keypad5': uinput.KEY_KP5,
            'keypad6': uinput.KEY_KP6, 'keypad7': uinput.KEY_KP7,
            'keypad8': uinput.KEY_KP8, 'keypad9': uinput.KEY_KP9,
            'keypad0': uinput.KEY_KP0, 'period': uinput.KEY_DOT,
            'capslock': uinput.KEY_CAPSLOCK, 'numlock': uinput.KEY_NUMLOCK,
            'backspace': uinput.KEY_BACKSPACE, 'pause': uinput.KEY_PAUSE,
            'scrolllock': uinput.KEY_SCROLLLOCK, 'backquote': uinput.KEY_GRAVE,
            'comma': uinput.KEY_COMMA, 'minus': uinput.KEY_MINUS,
            'slash': uinput.KEY_SLASH, 'semicolon': uinput.KEY_SEMICOLON,
            'equals': uinput.KEY_EQUAL, 'backslash': uinput.KEY_BACKSLASH,
            'kp_period': uinput.KEY_KPDOT, 'kp_equals': uinput.KEY_KPEQUAL,
            'a': uinput.KEY_A, 'b': uinput.KEY_B, 'c': uinput.KEY_C,
            'd': uinput.KEY_D, 'e': uinput.KEY_E, 'f': uinput.KEY_F,
            'g': uinput.KEY_G, 'h': uinput.KEY_H, 'i': uinput.KEY_I,
            'j': uinput.KEY_J, 'k': uinput.KEY_K, 'l': uinput.KEY_L,
            'm': uinput.KEY_M, 'n': uinput.KEY_N, 'o': uinput.KEY_O,
            'p': uinput.KEY_P, 'q': uinput.KEY_Q, 'r': uinput.KEY_R,
            's': uinput.KEY_S, 't': uinput.KEY_T, 'u': uinput.KEY_U,
            'v': uinput.KEY_V, 'w': uinput.KEY_W, 'x': uinput.KEY_X,
            'y': uinput.KEY_Y, 'z': uinput.KEY_Z
            }

    return keymap


def generate_keylist():
    """generate a list of keys we actually need
    this will be stored in memory and will comprise of
    a,b,x,y,start,select,l,r,left,right,up,down,l2,r2,l3,r3
    keyboard corresponding values the user has chosen
    in the retroarch.cfg file"""

    keylist = []
    key_bindings = get_key_bindings('/opt/retropie/configs/all/retroarch.cfg')
    keymap = get_keymap()
    errors = []

    for binding in key_bindings:

        try:
            keylist.append(keymap[binding])
        except KeyError as e:
            errors.append(e)

    if (len(errors) > 0):
        print 'The %s keys in your retroarch.cfg are unsupported\
                by this script\n' % ', '.join(map(str, errors))
        print 'Supported keys are:\n'
        print get_keymap().keys()
        sys.exit()

    return keylist


def get_key_bindings(ra_cfg):
    """read key mappings from retroarch.cfg file.
    returns the corresponding keys the user mapped
    in the retroarch.cfg file"""

    keys = []
    with open(ra_cfg, 'r') as fp:
        for line in fp:
            if 'input_player1_' in line and '#' not in line and \
            'btn' not in line and 'axis' not in line and \
            'index' not in line and 'mode' not in line and \
            'l2' not in line and 'r2' not in line and \
            'l3' not in line and 'r3' not in line and \
            'l_' not in line and 'r_' not in line and \
            'turbo' not in line:
                keys.append(line.split('=')[1][2:-2])
    return keys


def register_device(keylist):

    return uinput.Device(keylist)


def press_keys(line, device, keylist):
    """Emulate keyboard presses when a mapped button on the remote control
    has been pressed.

    To navigate, only a,b,x,y,start,select,up,down,left,right and escape are required
    """

    if "SetCurrentButton" in line:

        if "left" in line:

            device.emit(keylist[6], 1)
            sleep(0.02)
            device.emit(keylist[6], 0)

        elif "right" in line:

            device.emit(keylist[7], 1)
            sleep(0.02)
            device.emit(keylist[7], 0)

        elif "up" in line:

            device.emit(keylist[8], 1)
            sleep(0.02)
            device.emit(keylist[8], 0)

        elif "down" in line:

            device.emit(keylist[9], 1)
            sleep(0.02)
            device.emit(keylist[9], 0)

        elif "select" in line or "red" in line:

            device.emit(keylist[4], 1)
            device.emit(keylist[0], 1)
            sleep(0.02)
            device.emit(keylist[4], 0)
            device.emit(keylist[0], 0)

        elif "green" in line:

            device.emit(keylist[1], 1)
            sleep(0.02)
            device.emit(keylist[1], 0)

        elif "exit" in line:

            device.emit(keylist[1], 1)
            device.emit(keylist[5], 1)
            sleep(0.02)
            device.emit(keylist[1], 0)
            device.emit(keylist[5], 0)

        elif "yellow" in line:

            device.emit(keylist[2], 1)
            sleep(0.02)
            device.emit(keylist[2], 0)

        elif "blue" in line:

            device.emit(keylist[3], 1)
            sleep(0.02)
            device.emit(keylist[3], 0)

        elif "21" in line:

            device.emit(keylist[10], 1)
            sleep(0.02)
            device.emit(keylist[10], 0)

        elif "play" in line:

            device.emit(keylist[11], 1)
            sleep(0.02)
            device.emit(keylist[11], 0)

        elif "pause" in line:

            device.emit(keylist[12], 1)
            sleep(0.02)
            device.emit(keylist[12], 0)

        # Uncomment the prinnt statement below to display remote output
        #print line


def main():

    keylist = generate_keylist()
    device = register_device(keylist)
    p = subprocess.Popen('cec-client', stdout=subprocess.PIPE, bufsize=1)
    lines = iter(p.stdout.readline, b'')
    for line in lines:
        press_keys(line, device, keylist)

if __name__ == "__main__":
    main()
