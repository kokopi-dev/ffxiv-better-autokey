#!/usr/bin/python3
"""
process_exec contains a class with process and helper functions,
contains finding process and executing auto keystrokes
"""
import re
import time
import psutil
import json
import sys
from pywinauto.application import Application
from pywinauto.keyboard import *

class ProcessExec:
    """
    """
    def __init__(self):
        self.process_input = process_input

    def connect_process(process_input):
        """
        """

        try:
            app = Application().connect(process=process_input)
        except NameError:
            print("  <Error: Process not found.>\n  ... Either make sure FFXIV is running or change 'process_name'")
            sys.exit()

        return app

    def auto_pid(process_input):
        """
        """
        for proc in psutil.process_iter():
            if proc.name() == process_input:
                findingPID = re.search('pid=(.+?), name=', str(proc))
                catch_pid = int(findingPID.group(1))

        return catch_pid

    def auto_craft(process_input, json_data):
        """
        """

        while True:
            time.sleep(3)
            # SELECT "SYNTHESIZE"
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
            print("  ... Selecting the button 'Synthesize'.")
            time.sleep(3)
            # PRESS "SYNTHESIZE"
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
            print("  ... Pressing the button 'Synthesize'.")
            time.sleep(3)
            # CRAFTING MACRO 1
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k1"])
            print("  ... Pressing macro 1 ... <wait.{:d}>.".format(json_data["m1"]))
            time.sleep(json_data["m1"])
            # CRAFTING MACRO 2
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k2"])
            print("  ... Pressing macro 2 ... <wait.{:d}>.".format(json_data["m2"]))
            time.sleep(json_data["m2"])

    def auto_craft_buff(process_input, json_data, food, pot):
        """
        """
        food_loss = 0
        pot_loss = 0
        while True:
            # AUTO POT BUFF SEQUENCE
            if pot_loss >= pot:
                time.sleep(1)
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_ESCAPE}')
                print("  ... STANDING UP BY EXITING")
                time.sleep(4)
                # POT KEY
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k3"])
                print("  ... EATING FOOD")
                time.sleep(2)
                # CRAFT ITEM BUTTON
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k5"])
                print("  ... SELECTING CRAFT")
                time.sleep(3)
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
                print("  ... HIGHLIGHT SELECT CRAFT")
                time.sleep(2)
                pot_loss = 0
                # default 15 min pot buff minus 30 seconds
                pot = 870
            # AUTO FOOD BUFF SEQUENCE
            if food_loss >= food:
                time.sleep(1)
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_ESCAPE}')
                print("  ... STANDING UP BY EXITING")
                time.sleep(4)
                # FOOD KEY
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k4"])
                print("  ... EATING FOOD")
                time.sleep(2)
                # CRAFT ITEM BUTTON
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k5"])
                print("  ... SELECTING CRAFT")
                time.sleep(3)
                process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
                print("  ... HIGHLIGHT SELECT CRAFT")
                time.sleep(2)
                pot_loss = 0
                # default 30 min pot buff minus 30 seconds
                food = 1770
            time.sleep(3)
            food_loss += 3
            pot_loss += 3
            # SELECT "SYNTHESIZE"
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
            print("  ... Selecting the button 'Synthesize'.")
            time.sleep(3)
            food_loss += 3
            pot_loss += 3
            # PRESS "SYNTHESIZE"
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes('{VK_NUMPAD0}')
            print("  ... Pressing the button 'Synthesize'.")
            time.sleep(3)
            food_loss += 3
            pot_loss += 3
            # CRAFTING MACRO 1
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k1"])
            print("  ... Pressing macro 1 ... <wait.{:d}>.".format(json_data["m1"]))
            time.sleep(json_data["m1"])
            food_loss += json_data["m1"]
            pot_loss += json_data["m1"]
            # CRAFTING MACRO 2
            process_input.window(title='FINAL FANTASY XIV').send_keystrokes(json_data["k2"])
            print("  ... Pressing macro 2 ... <wait.{:d}>.".format(json_data["m2"]))
            time.sleep(json_data["m2"])
            food_loss += json_data["m2"]
            pot_loss += json_data["m2"]
