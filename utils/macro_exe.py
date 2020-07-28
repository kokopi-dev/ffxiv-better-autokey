#!/usr/bin/env python3
import ui.settings as s
import json
import os
BEFORE_KEY = 1
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
	for v in macro.values():
		total_wait += v["wait"]
	total_wait += BEFORE_KEY
	total_wait += AFTER_COLLECT_MENU
	return total_wait * amt

def use_macro(macro: dict, amt: int, flags: list):
    """Uses the selected macro on a set amt of cycles.
    macro returns None if there is no macro read.
    macro format: check parse_macro() docstring.
    Args:
        macro: Comes from read_macro()
    """
    options = {
        "-collect": False
    }
    for f in flags:
        if options.get(f, "") != "":
            options[f] = True
    proc = Process()
    select = "{VK_NUMPAD0}"
    for i in range(amt):
        #print(f" > Craft #{i}")
        for i in range(4):
            proc.press_key(select)
        sleep(BEFORE_KEY)
        for step in macro:
            wait = macro[step]["wait"]
            key = macro[step]["key"]
            #print(f"   > Pressing {key}")
            proc.press_key(key)
            #print(f"   > Waiting {wait}s")
            sleep(wait)
        if options["-collect"] == True:
            #print(f"   > Collectable Menu")
            for i in range(4):
                proc.press_key(select)
            sleep(AFTER_COLLECT_MENU)
    #print("Crafts finished.")