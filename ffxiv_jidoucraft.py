#!/usr/bin/env python3
"""Entry point for the crafting automater"""
import sys
from json_editor import json_reader
from process import Process
from time import sleep
from win10toast import ToastNotifier

def notifier(title=None, message=None):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=7)

def args_checker():
    accepted_args = ["foodbuff", "potbuff", "collectable", "limit", "notify", "--help"]
    args = sys.argv[1:]
    all_ok = 0
    for arg in args:
        if arg in accepted_args:
            all_ok += 1
    if all_ok != len(args):
        print("Incorrect argument(s). Choose from this list:\n{}\n".format(accepted_args))
        quit()
    return args

def int_validator(value=None):
    if value != None:
        try:
            value = int(value)
        except ValueError:
            print("Error: Input needs to be a number. Restart ffxiv_jidoucraft.py.")
            quit()
        return value

if __name__ == "__main__":
    json_data = json_reader()
    ffxiv = Process(json_data["process_name"])

    args = args_checker()
    if "--help" in args:
        with open("help.txt", "r") as f:
            helper = f.read()
            print(helper)
        quit()

    just_buffed = 0

    foodbuff = 0
    food_time = None
    food_limiter = 0

    potbuff = 0
    pot_time = None
    pot_limiter = 0

    collectable = 0

    craft_counter = 0
    craft_amount = None

    macro_amount = json_data["macro_amount"]
    timer_list = ["m1", "m2", "m3", "m4"]
    button_list = ["k1", "k2", "k3", "k4"]

    notify = 0

    if "notify" in args:
        notify = 1
    if "foodbuff" in args:
        print("Adding foodbuffer to crafting automation...")
        food_time = input("What is your current food buff time?\n")
        food_time = int_validator(food_time)
        foodbuff = 1
    if "potbuff" in args:
        print("Adding potbuffer to crafting automation...")
        pot_time = input("What is your current pot buff time?\n")
        pot_time = int_validator(pot_time)
        potbuff = 1
    if "collectable" in args:
        print("Collectable mode activated...")
        collectable = 1
    if "limit" in args:
        print("How many crafts do you want to limit to?")
        craft_amount = input()
        try:
            craft_amount = int(craft_amount)
        except ValueError:
            print("  -> ERROR: Enter a number. Run ffxiv_jidoucraft.py again.")
            quit()
        m_time = 0
        for i in range(macro_amount):
            m_time += json_data[timer_list[i]]
            m_time += 8 # Numpad 0 presses estimated amount of time it takes
        res = (craft_amount * m_time) / 60
        print("  -> Estimated completion time: {:.2f} minutes.".format(res))

    # Regular auto-craft
    print("Starting crafting automation...")
    print("TO QUIT: PRESS CTRL+C")
    print("\nMake sure your MOUSE CURSOR is HIGHLIGHTING THE CRAFT ITEM BEFORE MINIMIZING\n")
    print("\nMake sure your MOUSE CURSOR is NOT HIGHLIGHTING ANYTHING BEFORE MINIMIZING\n")
    while True:
        if "limit" in args:
            print("Craft #{}".format(craft_counter + 1))
            if craft_counter >= craft_amount:
                print("Crafted {} times, quitting program.".format(craft_amount))
                if notify == 1:
                    notify_message = "Crafted {} times.".format(craft_amount)
                    notifier("Crafting Batch Finished", notify_message)
                quit()

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
        for zero_counter in range(10):
            ffxiv.press_key("{VK_NUMPAD0}")
        sleep(2)
        food_limiter += 4
        pot_limiter += 4

        if collectable == 1:
            print("  -> Collectable mode selected, please wait.")
            for zero_counter in range(15):
                ffxiv.press_key("{VK_NUMPAD0}")
            sleep(2)
            food_limiter += 4
            pot_limiter += 4

        for i in range(macro_amount):
            ffxiv.press_key(json_data[button_list[i]])
            print("  -> Pressing Macro {}".format(i + 1))
            print("    -> Waiting {} seconds.".format(json_data[timer_list[i]]))
            sleep(json_data[timer_list[i]])
            food_limiter += json_data[timer_list[i]]
            pot_limiter += json_data[timer_list[i]]

        sleep(3)
        food_limiter += 3
        pot_limiter += 3
        craft_counter += 1
