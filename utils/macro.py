#!/usr/bin/env python3
import os
from pathlib import Path
import json
import re
from utils.process import Process
from time import sleep
CWDPATH = os.getcwd()
ABSPATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(Path(ABSPATH).parent, ".profiles.json")


def read_all_macro() -> dict:
    """Creates a config file if not exists, then returns entire file in dict"""
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            f.write("{}")
    with open(CONFIG_PATH, "r") as f:
            return json.load(f)

def parse_macro(filetext: list) -> dict:
    res = {}
    step = 0
    re_wait = re.compile(r"<wait.(.+?)>")
    re_key = re.compile(r"KEY")
    temp = 3 # Time padding for misclicks
    for line in filetext:
        wait = re_wait.findall(line)
        # Finding key push
        if wait == [] and re_key.findall(line) == ["KEY"]:
            res[step] = {}
            key = line.split()[1]
            res[step]["key"] = key
        # Finding next key push
        elif line == "\n":
            res[step]["wait"] = temp
            temp = 3
            step += 1
        else:
            temp += int(wait[0])
    res[step]["wait"] = temp
    return res

def make_macro(filename: str):
    """Writes to CONFIG_PATH, adds new macro to current macro list"""
    if not os.path.exists(filename):
        print("ERROR: Filename does not exist in this directory")
        quit()
    all_macros = read_all_macro()
    filepath = os.path.join(CWDPATH, filename)
    macroname = os.path.splitext(filename)[0]
    with open(filepath, "r") as f:
        macro = parse_macro(f.readlines())
    with open(CONFIG_PATH, "w+") as f:
        all_macros[macroname] = macro
        json.dump(all_macros, f)
        print(f"Created macro profile: {macroname}")

def read_macro(name: str) -> list:
    if not os.path.exists(CONFIG_PATH):
        print("ERROR: No profiles have been made. Use the command 'make'")
        quit()
    with open(CONFIG_PATH, "r") as f:
        macro = json.load(f).get(name, None)
        return macro

def delete_macro(name: str):
    """TODO: Error handle better.
    Reads macro first to check if profile exists.
    """
    macro = read_macro(name)
    macros = read_all_macro()
    if macro:
        del macros[name]
        print(f"Deleted macro profile: {name}")

def use_macro(macro: dict, amt: int):
    """Uses the selected macro on a set amt of cycles.
    Args:
        macro: Comes from read_macro()
    """
    if not macro:
        print("ERROR: Macro name does not exist your profiles")
        quit()
    print(f"Starting {amt} crafts:")
    proc = Process()
    select = "{VK_NUMPAD0}"
    for i in range(amt):
        print(f" > Craft #{i}")
        for i in range(4):
            proc.press_key(select)
        sleep(0.5)
        for step in macro:
            wait = macro[step]["wait"]
            key = macro[step]["key"]
            print(f"   > Pressing {key}")
            proc.press_key(key)
            print(f"   > Waiting {wait}s")
            sleep(wait)
    print("Crafts finished.")

def list_macros():
    macros = read_all_macro()
    if macros != {}:
        print("Current macro profiles:")
        for m in macros:
            print(f"  {m}")
    else:
        print("Make a macro profile with the 'make' command")
    quit()