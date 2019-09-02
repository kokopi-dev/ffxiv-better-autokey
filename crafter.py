#!/usr/bin/env python3
"""Entry point for the crafting automater"""
import sys
from json_editor import json_reader
from process import Process
from time import sleep
from win10toast import ToastNotifier


class AutoCraft:
    def __init__(self, json_data=None, mode=None):
        self.opt_help = 0
        self.opt_foodbuff = 0
        self.opt_potbuff = 0
        self.opt_collectable = 0
        self.opt_limit = 0
        self.opt_notify = 0
        self.opt_repair = 0
        self.flask = 0
        # if flask becomes 1, use bottom 3
        self.food_time = 0
        self.craft_amount = 0
        self.pot_time = 0
        self.json_data = json_data
        if self.json_data:
            self.ffxiv = Process(self.json_data["process_name"])
            self.macro_amount = self.json_data["macro_amount"]
            self.timer_list = ["m1", "m2", "m3", "m4"]
            self.button_list = ["k1", "k2", "k3", "k4"]
        else:
            print("ERROR: JSON file not found. Try running setup.py")
        if self.flask == 0:
            self.crafter()

    def args_checker(self):
        accepted_args = ["repair", "foodbuff", "potbuff", "collectable", "limit", "notify", "--help"]
        args = sys.argv[1:]
        all_ok = 0
        if "flask" in set(args):
            self.flask = 1
            try:
                with open("automation_settings.json", "r") as f:
                    data = json.load(f)
                    self.food_time = data["temp_food_time"]
                    self.craft_amount = data["temp_craft_amount"]
                    self.pot_time = data["temp_pot_time"]
            except FileNotFoundError:
                print("ERROR: Requires automation_settings.json")
                quit()
        for arg in args:
            if arg == "flask":
                all_ok += 1
            if arg == "--help":
                self.opt_help = 1
                all_ok += 1
            if arg == "repair":
                self.opt_repair = 1
                all_ok += 1
            if arg == "foodbuff":
                self.opt_foodbuff = 1
                all_ok += 1
            if arg == "potbuff":
                self.opt_potbuff = 1
                all_ok += 1
            if arg == "collectable":
                self.opt_collectable = 1
                all_ok += 1
            if arg == "limit":
                self.opt_limit = 1
                all_ok += 1
            if arg == "notify":
                self.opt_notify = 1
                all_ok += 1
        if all_ok != len(args):
            print("Incorrect argument(s). Choose from this list:\n{}\n".format(accepted_args))
            quit()

    def notifier(self, title=None, message=None):
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=7)

    def int_validator(self, value=None):
        if value != None:
            try:
                value = int(value)
            except ValueError:
                print("Error: Input needs to be a number. Restart ffxiv_jidoucraft.py.")
                quit()
            return value

    def time_estimater(self, json_data, craft_amount):
        m_time = 0
        for i in range(self.macro_amount):
            m_time += self.json_data[self.timer_list[i]]
            m_time += 8 # Numpad 0 presses estimated amount of time it takes
        res = (craft_amount * m_time) / 60
        print("  -> Estimated completion time: {:.2f} minutes.".format(res))

    def auto_end(self, craft_count, craft_amount):
        print("Crafted {} times, quitting program.".format(craft_amount))
        if self.opt_notify == 1:
            notify_message = "Crafted {} times.".format(craft_amount)
            self.notifier("Crafting Batch Finished", notify_message)
        quit()

    def auto_foodbuff(self):
        print("  -> Standing up by pressing ESC")
        for esc_counter in range(12):
            self.ffxiv.press_key("{VK_ESCAPE}")
        sleep(2)
        print("  -> Eating food")
        for food_counter in range(2):
            self.ffxiv.press_key(self.json_data["food_key"])
        sleep(7)

    def auto_potbuff(self):
        print("  -> Standing up by pressing ESC")
        for esc_counter in range(12):
            self.ffxiv.press_key("{VK_ESCAPE}")
        sleep(2)
        print("  -> Eating pot")
        for food_counter in range(2):
            self.ffxiv.press_key(self.json_data["pot_key"])
        sleep(7)

    def auto_repair(self):
        print("  -> Standing up by pressing ESC")
        for esc_counter in range(12):
            self.ffxiv.press_key("{VK_ESCAPE}")
        sleep(2)
        print("  -> Pressing repair menu")
        self.ffxiv.press_key("q")
        sleep(0.1)
        self.ffxiv.press_key("{VK_NUMPAD0}")
        sleep(0.1)
        self.ffxiv.press_key("{VK_NUMPAD6}")
        self.ffxiv.press_key("{VK_NUMPAD0}")
        self.ffxiv.press_key("{VK_ESCAPE}")
        sleep(8)

    def crafter(self):
        self.args_checker()
        if self.opt_help == 1:
            with open("help.txt", "r") as f:
                helper = f.read()
                print(helper)
            quit()

        just_buffed = 0
        repair_limiter = 0

        foodbuff = 0
        food_time = None
        food_limiter = 0

        potbuff = 0
        pot_time = None
        pot_limiter = 0

        collectable = 0

        craft_counter = 0
        craft_amount = None

        notify = 0

        if self.opt_notify == 1:
            notify = 1
        if self.opt_foodbuff == 1:
            print("Adding foodbuffer to crafting automation...")
            if self.flask == 1:
                food_time = self.food_time
            else:
                food_time = input("What is your current food buff time?\n")
                food_time = self.int_validator(food_time)
            foodbuff = 1
        if self.opt_potbuff == 1:
            print("Adding potbuffer to crafting automation...")
            if self.flask == 1:
                pot_time = self.pot_time
            else:
                pot_time = input("What is your current pot buff time?\n")
                pot_time = self.int_validator(pot_time)
            potbuff = 1
        if self.opt_collectable == 1:
            print("Collectable mode activated...")
        if self.opt_limit == 1:
            print("How many crafts do you want to limit to?")
            if self.flask == 1:
                craft_amount = self.craft_amount
            else:
                craft_amount = input()
                try:
                    craft_amount = int(craft_amount)
                except ValueError:
                    print("  -> ERROR: Enter a number. Run ffxiv_jidoucraft.py again.")
                    quit()
            self.time_estimater(self.json_data, craft_amount)
        if self.opt_repair == 1:
            print("Auto repair activated...")

        # Regular auto-craft
        print("Starting crafting automation...")
        print("TO QUIT: PRESS CTRL+C")
        while True:
            if self.opt_limit == 1:
                if craft_counter >= craft_amount:
                    self.auto_end(craft_counter, craft_amount)
                print("Craft #{}".format(craft_counter + 1))

            if self.opt_repair == 1:
                if repair_limiter >= 2280:
                    self.auto_repair()
                    repair_limiter = 0

            if foodbuff == 1:
                if food_limiter >= food_time:
                    self.auto_foodbuff()
                    food_limiter = 0
                    food_time = 1770 # Default 30 min pot buff minus 30 seconds
                    just_buffed += 1
            if potbuff == 1:
                if pot_limiter >= pot_time:
                    self.auto_potbuff()
                    pot_limiter = 0
                    pot_time = 870 # Default 15 min pot buff minus 30 seconds
                    just_buffed += 1

            if just_buffed >= 1:
                print("  -> Selecting Craft")
                self.ffxiv.press_key(self.json_data["craft_key"])
                just_buffed = 0

            sleep(0.01)
            print("  -> Pressing + Selecting 'Synthesis'")
            for i in range(4):
                self.ffxiv.press_key("{VK_NUMPAD0}")

            sleep(0.5)
            food_limiter += 2
            pot_limiter += 2
            repair_limiter += 2

            if self.opt_collectable == 1:
                print("  -> Collectable mode selected, please wait.")
                for zero_counter in range(6):
                    self.ffxiv.press_key("{VK_NUMPAD0}")
                sleep(0.5)
                food_limiter += 2
                pot_limiter += 2
                repair_limiter += 2

            for i in range(self.macro_amount):
                self.ffxiv.press_key(self.json_data[self.button_list[i]])
                print("  -> Pressing Macro {}".format(i + 1))
                print("    -> Waiting {} seconds.".format(self.json_data[self.timer_list[i]]))
                sleep(self.json_data[self.timer_list[i]])
                food_limiter += self.json_data[self.timer_list[i]]
                pot_limiter += self.json_data[self.timer_list[i]]
                repair_limiter += self.json_data[self.timer_list[i]]

            sleep(3)
            food_limiter += 3
            pot_limiter += 3
            repair_limiter += 3
            craft_counter += 1

if __name__ == "__main__":
    json_data = json_reader()
    ff = AutoCraft(json_data)
