#!/usr/bin/env python3
import utils.settings as s
import sys
import os
import json


def check_profile_exists(profile):
    if profile not in list(s.PROFILES):
        sys.stderr.write(s.ERROR_CHECK_0.format(profile))
        sys.exit()

def check_integer(number):
    if not number.isdigit() or int(number) < 0:
        sys.stderr.write(s.ERROR_CHECK_1)
        sys.exit()

def check_options(options):
    for o in options:
        if o not in s.FLAGS:
            sys.stderr.write(s.ERROR_CHECK_2.format(o))
            sys.exit()

def check_path(filepath):
    if not os.path.exists(filepath):
        return False
    return True

def last_path(filepath):
    if os.sep in filepath:
        return filepath.split(os.sep)[-1]
    return filepath

def read_json(path) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def write_json(path, data: dict):
    with open(path, "w+") as f:
        json.dump(data, f)

def get_macro(name: str) -> dict:
    """
    profiles template:
    macro_name: {last_updated: 0, macro:{keys: [], wait: []}, filepath: string}
    """
    if not check_path(s.CONFIG_PATH):
        sys.stderr.write(s.ERROR_CHECK_3)
        sys.exit()
    with open(CONFIG_PATH, "r") as f:
        macro = json.load(f).get(name, None)
        return macro

def parse_wait(line):
    """Regex to find wait time on macro line
    Returns:
        Int if regex found
        None if newline
    """
    timer = s.RE_WAIT.findall(line)
    if timer != []:
        return int(timer[0])

def parse_key(line):
    """Regex to find wait time on macro line
    Returns:
        str if regex found
        None if not a KEY
    """
    check = s.RE_KEY.findall(line)
    if check != []:
        key = line.split()[1]
        return key

def update_macro(macroname, filepath):
    """Updates profiles json"""
    s.PROFILES[macroname] = {}
    s.PROFILES[macroname]["updated_at"] = os.stat(filepath).st_mtime
    s.PROFILES[macroname]["path"] = filepath
    macro = {"keys": [], "wait": []}
    with open(filepath, "r") as f:
        for line in f.readlines():
            key = parse_key(line)
            wait = parse_wait(line)
            if key:
                macro["keys"].append(key)
                key_idx = len(macro["keys"]) - 1
                macro["wait"].append(0)
            if wait:
                macro["wait"][key_idx] += wait
    s.PROFILES[macroname]["macro"] = macro
    write_json(s.PROFILES_PATH, s.PROFILES)

def get_time_estimation(macro, amt):
    steps = len(macro["macro"]["keys"])
    steps_sleep = steps * (s.CRAFT_SLEEPS["step1"] + s.CRAFT_SLEEPS["step2"])
    input_sleep = s.CRAFT_SLEEPS["input1"] + s.CRAFT_SLEEPS["input2"]
    total_wait = 0
    for idx in range(steps):
        total_wait += macro["macro"]["wait"][idx]
    seconds = (amt * total_wait) + (amt * steps_sleep) + (amt * input_sleep)
    minutes = (seconds / 60)
    return minutes

def scan_macros():
    """Scans macros folder, adds new macro files, updates profiles files,
    updates logs file"""
    # Cross check current files and profiles.json files, update, add, delete
    logs = read_json(s.LOGS_PATH)
    macros_folder = os.path.join(s.CWDPATH, s.MACROS_FOLDER)
    files = os.listdir(macros_folder)
    files.remove("README.txt") # README.txt required in this folder
    profiles_list = [f.replace(".txt", "") for f in files]
    for profile in profiles_list:
        if s.PROFILES.get(profile, "") != "":
            # Profile exists in profiles.json, check timestamps
            old_timestamp = s.PROFILES[profile]["updated_at"]
            curr_timestamp = os.stat(s.PROFILES[profile]["path"]).st_mtime
            if curr_timestamp != old_timestamp:
                update_macro(profile, s.PROFILES[profile]["path"])
        else:
            # Profile does not exist in profiles.json
            name = profile + ".txt"
            fpath = os.path.join(macros_folder, name)
            update_macro(profile, fpath)
            s.LOGS["added"].append(profile)
    # Check for deleted txt files
    for item in s.LOGS["added"]:
        if item not in profiles_list:
            del s.PROFILES[item]
            write_json(s.PROFILES_PATH, s.PROFILES)
            s.LOGS["added"].remove(item)
    write_json(s.LOGS_PATH, s.LOGS)

def setup():
    if not check_path(s.PROFILES_PATH):
        write_json(s.PROFILES_PATH, {})
    if not check_path(s.MACROS_FOLDER):
        os.mkdir(s.MACROS_FOLDER)
    if not check_path(s.LOGS_PATH):
        write_json(s.LOGS_PATH, {"added": []})
