#!/usr/bin/env python3
"""Setup for program settings.

Creates a json if does not exists.
"""
import os
import json

abs_path = os.path.dirname(os.path.abspath(__file__))
json_file_name = "automation_settings.json"
json_file_path = abs_path + "\\" + json_file_name
json_template = {"m1": 46, "m2": 46, "m3": 0, "m4": 0, "k1": "1", "k2": "2", "k3": "3", "k4": "4", "process_name": "ffxiv_dx11.exe", "food_key": "4", "pot_key": "5", "craft_key": "~", "macro_amount": 2}

def setup():
    print("Setting up the crafting automater for FFXIV...")

    if not os.path.exists(json_file_path):
        with open(json_file_name, "w") as f:
            json.dump(json_template, f)
        print("Done.")
    else:
        print("  -> File settings.json already exists...")
        pass

if __name__ == "__main__":
    setup()
