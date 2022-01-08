#!/usr/bin/env python3

def parse_macro_line(line):
    key, wait = None, None
    key_check = self.REGEX_KEY.findall(line)
    wait_check = self.REGEX_WAIT.findall(line)

    if key_check != []:
        key = line.split()[1]
    if wait_check != []:
        wait = int(wait_check[0])

    return key, wait

def parse_update_macro(fp: str):
    macro = {"keys": [], "wait": []}
    key_idx = 0
    with open(fp, "r", encoding="utf8", errors="ignore") as f:
        for line in f.readlines():
            key, wait = parse_macro_line(line)
            if key:
                macro["keys"].append(key)
                key_idx = len(macro["keys"]) - 1
                macro["wait"].append(0)
            if wait:
                macro["wait"][key_idx] += wait
    return macro
