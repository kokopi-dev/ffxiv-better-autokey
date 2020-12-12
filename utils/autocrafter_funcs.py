#!/usr/bin/env python3
"""TODO, create profile_list as global var
"""
import utils.helpers as h
import utils.input_handler as input_handler
import utils.settings as s
import utils.notifications as notify
from utils.process import Process
from time import sleep
import os
import sys


def list_macros(args):
    sys.stdout.write(f"Available macros: {list(s.PROFILES)}")

def opt_repair(proc):
    """Repairing rotation
    Sleep: 9.5s
    """
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

def opt_food(proc):
    pass

def opt_potion(proc):
    pass

def use_macro(args):
    """Uses the selected macro on a set amt of cycles.
    Args:
        macro: Comes from read_macro()
        flags: List of options like repairing, and collectables
    """
    inputs = input_handler.craft(args) #inputs has macro amt opt
    macro = inputs["macro"]
    for f in inputs["opt"]:
        if s.CRAFT_OPTS.get(f, "") != "":
            s.CRAFT_OPTS[f] = True
    print(f"Starting {inputs['amt']} crafts:")
    proc = Process()
    select = "{VK_NUMPAD0}"
    steps = len(macro["macro"]["keys"])
    repair_counter = 0
    # Can adjust sleeps according to lag
    est = h.get_time_estimation(macro, inputs["amt"])
    print(f" > Time estimation: {est:.2f} minutes.")
    for i in range(inputs["amt"]):
        print(f" > Craft #{i + 1}")
        for _ in range(4):
            proc.press_key(select)
        sleep(s.CRAFT_SLEEPS["input1"])
        for step in range(steps):
            wait = macro["macro"]["wait"][step]
            key = macro["macro"]["keys"][step]
            print(f"   > Pressing {key}")
            sleep(s.CRAFT_SLEEPS["step1"])
            proc.press_key(key)
            print(f"   > Waiting {wait}s")
            sleep(wait)
            sleep(s.CRAFT_SLEEPS["step2"])
        if repair_counter > s.REPAIR_COUNTER:
            if s.CRAFT_OPTS["-repair"] == True:
                print("Self repairing...")
                opt_repair(proc)
            repair_counter = 0
        repair_counter += 1
        sleep(s.CRAFT_SLEEPS["input2"])
    print("Crafts finished.")
    notify.finished()
    