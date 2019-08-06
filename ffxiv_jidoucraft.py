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
        print("  -> Pressing + Selecting 'Synthesis'")
        for zero_counter in range(10):
            ffxiv.press_key("{VK_NUMPAD0}")
        sleep(2)

        ffxiv.press_key(json_data["k1"])
        print("  -> Pressing Macro 1")
        print("    -> Waiting {} seconds.".format(json_data["m1"]))
        sleep(json_data["m1"])

        ffxiv.press_key(json_data["k2"])
        print("  -> Pressing Macro 2")
        print("    -> Waiting {} seconds.".format(json_data["m2"]))
        sleep(json_data["m2"])
