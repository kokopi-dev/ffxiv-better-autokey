#!/usr/bin/env python3
import ui.settings as s
import json
import os
from time import sleep
BEFORE_KEY = 1 # If laggy in game, make this higher
AFTER_COLLECT_MENU = 2


def read_json() -> dict:
    if not os.path.exists(s.JSON_FILE_NAME):
        with open(s.JSON_FILE_NAME, "w") as f:
            f.write("{}")
            return {}
    with open(s.JSON_FILE_NAME, "r") as f:
        return json.load(f)

def write_json(data: dict):
    with open(s.JSON_FILE_NAME, "w+") as f:
        json.dump(data, f)

def get_time_estimation(macro, amt):
    total_wait = 0
    total_wait += macro["wait1"]
    if macro.get("wait2", "") != "":
        total_wait += macro["wait2"]
    total_wait += BEFORE_KEY
    total_wait += AFTER_COLLECT_MENU
    return total_wait * amt

def use_macro(macro: dict, amt: int, flags: dict):
    """Only 2 macros at most, if new craft patch creates 3 macros max,
    restructure macro dict.
    """
    select = "{VK_NUMPAD0}"
    for i in range(amt):
        for i in range(4):
            s.FFXIV.press_key(select)
        sleep(BEFORE_KEY)
        s.FFXIV.press_key(macro["key1"])
        sleep(macro["wait1"])
        if macro.get("key2", "") != "":
            s.FFXIV.press_key(macro["key2"])
            sleep(macro["wait2"])
        if flags["collect"] == True:
            for i in range(4):
                s.FFXIV.press_key(select)
            sleep(AFTER_COLLECT_MENU)