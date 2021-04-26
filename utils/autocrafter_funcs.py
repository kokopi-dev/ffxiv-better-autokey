#!/usr/bin/env python3
"""TODO, create profile_list as global var
"""
import utils.helpers as h
import utils.settings as s
import utils.notifications as notify
from utils import input_handler
from utils import ocr
from utils.process import Process
from time import sleep
import os
import sys


def list_macros(args):
    sys.stdout.write(f"Available macros: {list(s.PROFILES)}")

def opt_repair(proc):
    """Sleep: 9.5s
    """
    for _ in range(4):
        proc.press_key(s.ESC)
    sleep(3)
    proc.press_key(s.REPAIR)
    sleep(0.5)
    proc.press_key(s.RIGHT)
    sleep(0.5)
    proc.press_key(s.SELECT)
    sleep(0.5)
    proc.press_key(s.LEFT)
    sleep(0.5)
    proc.press_key(s.SELECT)
    sleep(0.5)
    proc.press_key(s.ESC)
    sleep(3)
    proc.press_key(s.CRAFT_ITEM)
    sleep(1)

def opt_food(proc):
    for _ in range(4):
        proc.press_key(s.ESC)

def opt_potion(proc):
    for _ in range(4):
        proc.press_key(s.ESC)

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
    steps = len(macro["macro"]["keys"])
    repair_counter = 0
    # Can adjust sleeps according to lag
    est = h.get_time_estimation(macro, inputs["amt"])
    print(f" > Time estimation: {est:.2f} minutes.")
    for i in range(inputs["amt"]):
        print(f" > Craft #{i + 1}")
        for _ in range(4):
            proc.press_key(s.SELECT)
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

def auto_leve(*args, **kwargs):
    """
    check dimension settings
    run capture2text, get output
    parse output
        - keep track of placement to compare with last step
    move arrows correctly
    """
    amt = input_handler.leve()
    print(f"Starting {amt} auto leves...")
    for a in range(amt):
        proc = Process()
        proc.press_to_leve_menu_seq()
        idx = get_quest_index()
        print(f"found cookie quest index @ {idx}")
        proc.press_leve_menu_seq(idx)
        proc.press_tfocus_macro()
        proc.press_leve_quest_seq()
        proc.press_tnpc_macro()
