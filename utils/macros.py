#!/usr/bin/env python3
"""Inherited by BAKConfig, this is a little messy. update later"""
import os
import re
REGEX_WAIT = re.compile(r"<wait.(.+?)>")
REGEX_KEY = re.compile(r"KEY")


def parse_macro_line(line):
    key, wait = None, None
    key_check = REGEX_KEY.findall(line)
    wait_check = REGEX_WAIT.findall(line)

    if key_check != []:
        key = line.split()[1]
    if wait_check != []:
        wait = int(wait_check[0])

    return key, wait

class CraftMacroHandler:
    @classmethod
    def check_modified_macros(cls):
        has_changed = False
        allfiles = os.listdir(cls.craft_folder)
        allfiles = [os.path.join(cls.craft_folder, fp) for fp in allfiles]
        current_mod_config = {k: os.path.getmtime(k) for k in allfiles}
        last_mod_config = cls.config["craft"]["last_modified"]
        macros_config = cls.config["craft"]["macros"]

        if current_mod_config != last_mod_config:
            has_changed = True
            macros_config = {}

            for fp in allfiles:
                parsed_macro = cls._parse_update_macro(fp)
                macros_config[fp] = parsed_macro

        return has_changed, current_mod_config, macros_config

    @classmethod
    def _parse_update_macro(cls, fp: str):
        macro = {"keys": [], "wait": []}
        key_idx = 0
        with open(fp, "r") as f:
            for line in f.readlines():
                key, wait = parse_macro_line(line)
                if key:
                    macro["keys"].append(key)
                    key_idx = len(macro["keys"]) - 1
                    macro["wait"].append(0)
                if wait:
                    macro["wait"][key_idx] += wait
        return macro
