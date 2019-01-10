#!/usr/bin/python3
"""
Use the example to calculate sleep time:
YOUR_MACRO_WAIT_TOTAL + 5

You can manually edit the timers and keystrokes
in the .json file
"""
import json
import os
import sys
import psutil
import re
import time
from pywinauto.application import Application
from pywinauto.keyboard import *

#############
### Intro ###
#############
current_path = os.path.dirname(os.path.abspath(__file__))
# Opening json data file to read
with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
    macro_time = json.load(time_data)
# Displaying current macro timers
m_list = [macro_time["m1"], macro_time["m2"], macro_time["m3"], macro_time["m4"]]
print("The current macro timers are:\n")
print("m1\tm2\tm3\tm4")
print(*m_list, sep='\t')
# Displaying current keystrokes
k_list = [macro_time["k1"], macro_time["k2"], macro_time["k3"], macro_time["k4"]]
print("\nThe current keystrokes are:\n")
print("k1\tk2\tk3\tk4")
print(*k_list, sep='\t')

# argc, argv
argv = sys.argv[1:]
argc = len(argv)

# argument checker
if argc > 1:
    print("  <Error: Too many arguments (must be one).>")
    sys.exit()

if argc == 1 and sys.argv[1] != "edit" and sys.argv[1] != "editkeys":
    print("  <Error: %s command not found.>" % sys.argv[1])

editor = ""
editedTimerCount = 0
editedKeyCount = 0
try:
    # EDITING MACRO TIMERS
    if sys.argv[1] == "edit":
        editor = "y"
        while editor == "y":
            print("\nFormat example: m1 35")
            print("Which macro timer do you want to edit?")
            # User input
            editThis = input()
            print()

            try:
                if editThis == "":
                    print("  <Error: input cannot be none, try again.>")
                    sys.exit()
                if editThis[2] != ' ':
                    print("Wrong format.\nFormat example: m1 35")
                    sys.exit()
                if len(editThis) < 3:
                    print("Wrong format.\nFormat example: k1 3")
                    sys.exit()
            except IndexError:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()
            # Splitting input into macro and macro timer
            try:
                mtime = int(editThis[3:])
                m = editThis[:2]
            except:
                print("Wrong format.\nFormat example: m1 35")
                sys.exit()

            if m[0] != 'm':
                print("Wrong format.\nFormat example: m1 35")
                sys.exit()
            if mtime < 0 or mtime > 300:
                print("Wrong format.\nFormat example: m1 35\nTime limit is 300")
                sys.exit()

            # Temp adding to json
            with open("%s/ffxiv-autocraft_data.json" % current_path) as add_time_data:
                add_time = json.load(add_time_data)

            print("  ... editing requested macro timer.")
            add_time[m] = mtime

            # Saving to json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "w") as save_time_data:
                json.dump(add_time, save_time_data)
            # Rereading json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
                macro_time = json.load(time_data)
                print("  ... saving data...rereading data...done.")

            # Increment times edited
            editedTimerCount += 1

            # Continue or exit
            print("\nDo you want to edit another macro timer? (y/n)")
            editor = input()
            print()
            if editor == "y":
                pass
            elif editor == "n":
                print("  ... Program will continue to auto craft")
                break
            else:
                print(" <Error: input needs to be 'y' or 'n', exiting program.>")
                sys.exit()
    # EDITING KEYS
    elif sys.argv[1] == "editkeys":
        editor = "y"
        while editor == "y":
            acceptedKeys = ["1", "2", "3", "4", "5", "6", "7",
                            "8", "9", "0", "-", "="]
            acceptedPlace = ["k1", "k2", "k3", "k4"]

            print("\nAccepted key edits are the following:\n")
            print(' '.join(map(str, acceptedKeys)))
            print("\nFormat example: k1 3")
            print("Which keystroke do you want to edit?")
            # User input
            editThis = input()
            print()

            try:
                if editThis == "":
                    print("  <Error: input cannot be none, try again.>")
                    sys.exit()
                if editThis[2] != ' ':
                    print("Wrong format.\nFormat example: k1 3")
                    sys.exit()
                if len(editThis) < 3:
                    print("Wrong format.\nFormat example: k1 3")
                    sys.exit()
            except IndexError:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()

            # Splitting input into keys and keystrokes
            try:
                kstroke = str(editThis[3:])
                k = str(editThis[:2])
            except:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()

            if k not in acceptedPlace:
                print("Wrong format.\nFormat example: k1 3")
                sys.exit()
            if kstroke not in acceptedKeys:
                print("Keystroke not accepted, check accepted key edits above.")
                sys.exit()

            # Temp adding to json
            with open("%s/ffxiv-autocraft_data.json" % current_path) as add_key_data:
                add_key = json.load(add_key_data)

            print("  ... editing requested keystrokes.")
            add_key[k] = kstroke

            # Saving to json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "w") as save_key_data:
                json.dump(add_key, save_key_data)
            # Rereading json
            with open(("%s/ffxiv-autocraft_data.json" % current_path), "r") as time_data:
                macro_time = json.load(time_data)
                print("  ... saving data...rereading data...done.")

            # Increment times edited
            editedKeyCount += 1

            # Continue or exit
            print("\nDo you want to edit another keystroke? (y/n)")
            editor = input()
            print()
            if editor == "y":
                pass
            elif editor == "n":
                print("  ... Program will continue to auto craft")
                break
            else:
                print(" <Error: input needs to be 'y' or 'n', exiting program.>")
                sys.exit()
except IndexError:
    pass

# Displaying new timers if edited
if editedTimerCount > 0:
    m_list = [macro_time["m1"], macro_time["m2"], macro_time["m3"], macro_time["m4"]]
    print("\nThe new macro timers are:\n")
    print("m1\tm2\tm3\tm4")
    print(*m_list, sep='\t')

# Displaying new timers if edited
if editedKeyCount > 0:
    k_list = [macro_time["k1"], macro_time["k2"], macro_time["k3"], macro_time["k4"]]
    print("\nThe new keystrokes are:\n")
    print("k1\tk2\tk3\tk4")
    print(*k_list, sep='\t')

# Task Manager -> Right click FFXIV -> Go to details
process_name = "ffxiv_dx11.exe"

# AUTO PID
for proc in psutil.process_iter():
    if proc.name() == process_name:
        findingPID = re.search('pid=(.+?), name=', str(proc))
        ffxiv_pid = int(findingPID.group(1))

# If auto PID doesnt work, check if the 'process_name' is correct in your task manager`
try:
    app = Application().connect(process=ffxiv_pid)
except NameError:
    print("  <Error: Process not found.>\n  ... Either make sure FFXIV is running or change 'process_name'")
    sys.exit()

# Setup sleep times accordingly, and your keystrokes
print('\nPress Ctrl-C to quit crafting.')
try:
    while True:
        time.sleep(3)
        # SELECT "SYNTHESIZE"
        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
        print("  ... Selecting the button 'Synthesize'.")
        time.sleep(3)
        # PRESS "SYNTHESIZE"
        app.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
        print("  ... Pressing the button 'Synthesize'.")
        time.sleep(3)
        # CRAFTING MACRO 1
        app.window(title='FINAL FANTASY XIV').send_keystrokes(macro_time["k1"])
        print("  ... Pressing macro 1 ... <wait.{:d}>.".format(macro_time["m1"]))
        time.sleep(macro_time["m1"])
        # CRAFTING MACRO 2
        app.window(title='FINAL FANTASY XIV').send_keystrokes(macro_time["k2"])
        print("  ... Pressing macro 2 ... <wait.{:d}>.".format(macro_time["m2"]))
        time.sleep(macro_time["m2"])
except KeyboardInterrupt:
    print("Program has stopped.")
