#!/usr/bin/env python3
"""TODO, create profile_list as global var
"""
import utils.helpers as h
import utils.input_handler as input_handler
import utils.settings as s
from utils.process import Process
from time import sleep
import os
import sys


def create_macro(args):
    temp_input = input_handler.create(args)
    user_input = h.last_path(temp_input)
    filepath = os.path.join(s.CWDPATH, s.MACROS_FOLDER, user_input)
    if not h.check_path(filepath):
        print(f"ERROR: {user_input} does not exist in the macros\\ folder")
        sys.exit()
    macroname = user_input.replace(".txt", "")
    h.update_macro(macroname, filepath)
    print(f"Created profile: {user_input}")

def delete_macro(args):
    inputs = input_handler.delete(args)
    profile = inputs["profile"]
    if os.path.isfile(s.PROFILES[profile]["path"]):
        os.remove(s.PROFILES[profile]["path"])
    else:
        print("ERROR: Macro file does not exist.")
        sys.exit()
    del s.PROFILES[profile]
    h.write_json(s.PROFILES_PATH, s.PROFILES)
    logs = h.read_json(s.LOGS_PATH)
    del logs[profile]
    h.write_json(s.LOGS_PATH, logs)

def list_macros(args):
    print(f"Available macros: {list(s.PROFILES)}")

def opt_repair(proc):
    """Repairing rotation, 9.5s sleep"""
    select = "{VK_NUMPAD0}"
    esc = "{VK_ESCAPE}"
    left = "{LEFT}"
    right = "{RIGHT}"
    proc.press_key(esc)
    sleep(3)
    proc.press_key(s.REPAIR)
    sleep(0.5)
    proc.press_key(right)
    sleep(0.5)
    proc.press_key(select)
    sleep(0.5)
    proc.press_key(left)
    sleep(0.5)
    proc.press_key(select)
    sleep(0.5)
    proc.press_key(esc)
    sleep(3)
    proc.press_key(s.CRAFT_ITEM)
    sleep(1)

def use_macro(args):
    """Uses the selected macro on a set amt of cycles.
    Args:
        macro: Comes from read_macro()
        flags: List of options like repairing, and collectables
    """
    inputs = input_handler.craft(args) #inputs has macro amt opt
    macro = inputs["macro"]
    options = {
        "-repair": False,
        "-food": False,
        "-pot": False
    }
    for f in inputs["opt"]:
        if options.get(f, "") != "":
            options[f] = True
    print(f"Starting {inputs['amt']} crafts:")
    proc = Process()
    select = "{VK_NUMPAD0}"
    # TODO new macro layout
    steps = len(macro["macro"]["keys"])
    repair_counter = 0
    for i in range(inputs["amt"]):
        print(f" > Craft #{i + 1}")
        for _ in range(4):
            proc.press_key(select)
        sleep(1)
        for step in range(steps):
            wait = macro["macro"]["wait"][step]
            key = macro["macro"]["keys"][step]
            print(f"   > Pressing {key}")
            sleep(0.5)
            proc.press_key(key)
            print(f"   > Waiting {wait}s")
            sleep(wait)
            sleep(1)
        if repair_counter > s.REPAIR_COUNTER:
            if options["-repair"] == True:
                print("Self repairing...")
                opt_repair(proc)
            repair_counter = 0
        repair_counter += 1
        sleep(2.5)
    print("Crafts finished.")