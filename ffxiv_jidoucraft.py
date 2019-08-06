#!/usr/bin/env python3
"""Entry point for the crafting automater"""
import sys
from json_editor import json_reader
from process import Process
from time import sleep

def args_checker():
    accepted_args = ["foodbuff", "potbuff", "collectable"]
    args = sys.argv[1:]
    all_ok = 0
    for arg in args:
        if arg in accepted_args:
            all_ok += 1
    if all_ok != len(args):
        print("Incorrect argument(s). Choose from this list:\n{}\n".format(accepted_args))
        quit()
    return args

if __name__ == "__main__":
    json_data = json_reader()
    ffxiv = Process(json_data["process_name"])

    args = args_checker()
    just_buffed = 0

    foodbuff = 0
    food_time = None
    food_limiter = 0

    potbuff = 0
    pot_time = None
    pot_limiter = 0

    collectable = 0

    if "foodbuff" in args:
        print("Adding foodbuffer to crafting automation...")
        food_time = input("What is your current food buff time?\n")
        foodbuff = 1
    if "potbuff" in args:
        print("Adding potbuffer to crafting automation...")
        pot_time = input("What is your current pot buff time?\n")
        potbuff = 1
    if "collectable" in args:
        print("Collectable mode activated...")
        collectable = 1

    # Regular auto-craft
    print("Starting crafting automation...")
    print("TO QUIT: PRESS CTRL+C")
    print("\nMake sure your MOUSE CURSOR is HIGHLIGHTING THE CRAFT ITEM BEFORE MINIMIZING\n")
    print("\nMake sure your MOUSE CURSOR is NOT HIGHLIGHTING ANYTHING BEFORE MINIMIZING\n")
    while True:
        if foodbuff == 1:
            if food_limiter >= food_time:
                print("  -> Standing up by pressing ESC")
                for esc_counter in range(20):
                    ffxiv.press_key("{VK_ESCAPE}")
                sleep(5)
                print("  -> Eating food")
                for food_counter in range(3):
                    ffxiv.press_key(json_data["food_key"])
                sleep(7)
                food_limiter = 0
                food_time = 1770 # Default 30 min pot buff minus 30 seconds
                just_buffed += 1
        if potbuff == 1:
            if pot_limiter >= pot_time:
                print("  -> Standing up by pressing ESC")
                for esc_counter in range(20):
                    ffxiv.press_key("{VK_ESCAPE}")
                sleep(5)
                print("  -> Eating pot")
                for food_counter in range(3):
                    ffxiv.press_key(json_data["pot_key"])
                sleep(7)
                pot_limiter = 0
                pot_time = 870 # Default 15 min pot buff minus 30 seconds
                just_buffed += 1

        if just_buffed >= 1:
            print("  -> Selecting Craft")
            ffxiv.press_key(json_data["craft_key"])
            just_buffed = 0

        print("  -> Pressing + Selecting 'Synthesis'")
        for zero_counter in range(20):
            ffxiv.press_key("{VK_NUMPAD0}")
        sleep(2)
        food_limiter += 5
        pot_limiter += 5

        if collectable == 1:
            print("  -> Collectable mode selected, please wait.")
            for zero_counter in range(15):
                ffxiv.press_key("{VK_NUMPAD0}")
            sleep(2)
            food_limiter += 4
            pot_limiter += 4

        ffxiv.press_key(json_data["k1"])
        print("  -> Pressing Macro 1")
        print("    -> Waiting {} seconds.".format(json_data["m1"]))
        sleep(json_data["m1"])
        food_limiter += json_data["m1"]
        pot_limiter += json_data["m1"]

        ffxiv.press_key(json_data["k2"])
        print("  -> Pressing Macro 2")
        print("    -> Waiting {} seconds.".format(json_data["m2"]))
        sleep(json_data["m2"])
        food_limiter += json_data["m2"]
        pot_limiter += json_data["m2"]

        sleep(3)
        food_limiter += 3
        pot_limiter += 3
