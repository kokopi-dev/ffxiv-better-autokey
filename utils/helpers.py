#!/usr/bin/env python3
import utils.settings as s
import sys
import os
import json


def check_profile_exists(profile):
    if profile not in list(s.PROFILES):
        print(f"ERROR: {profile} does not exist, try creating it.")
        sys.exit()

def check_integer(number):
    if not number.isdigit() or int(number) < 0:
        print(f"ERROR: Please enter a positive number.")
        sys.exit()

def check_options(options):
    for o in options:
        if o not in s.FLAGS:
            print(f"ERROR: {o} is not an option.")
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
        print("ERROR: No profiles have been made. Use the command 'make'")
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
    log_timestamp(macroname, s.PROFILES[macroname]["updated_at"])

def log_timestamp(name, timestamp):
    logs = read_json(s.LOGS_PATH)
    logs[name] = timestamp
    write_json(s.LOGS_PATH, logs)

def refresh_timestamps():
    """Checks for any changes to macros"""
    logs = read_json(s.LOGS_PATH)
    if len(list(logs)) != 0:
        for macro in logs:
            s.PROFILES[macro]["updated_at"] = os.stat(s.PROFILES[macro]["path"]).st_mtime
            if logs[macro] != s.PROFILES[macro]["updated_at"]:
                update_macro(macro, s.PROFILES[macro]["path"])

def get_time_estimation(macro, amt):
    total_wait = 0
    total_wait += macro["wait1"]
    if macro.get("wait2", "") != "":
        total_wait += macro["wait2"]
    total_wait += s.BEFORE_KEY
    total_wait += s.AFTER_COLLECT_MENU
    return total_wait * amt

def setup():
    if not check_path(s.PROFILES_PATH):
        write_json(s.PROFILES_PATH, {})
    if not check_path(s.MACROS_FOLDER):
        os.mkdir(s.MACROS_FOLDER)
    if not check_path(s.LOGS_PATH):
        write_json(s.LOGS_PATH, {})