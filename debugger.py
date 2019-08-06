#!/usr/bin/env python3
from json_editor import json_reader
from process import Process
from time import sleep

if __name__ == "__main__":
    json_data = json_reader()
    ffxiv = Process(json_data["process_name"])

    # Regular auto-craft
    print("Starting crafting automation...")
    while True:
        a = input("pressing 0")
        ffxiv.press_key("{VK_NUMPAD0}")
        print("  -> Pressing")
