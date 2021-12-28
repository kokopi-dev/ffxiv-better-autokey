#!/usr/bin/env python3
"""Crafting related functionalities"""
import os
from time import sleep
import re
from typing import Optional, List
from utils.tty_colors import PrintColor as printc


class CraftConfig:
    """Craft Config settings -> inherited by the main config: BAKConfig"""
    REGEX_WAIT = re.compile(r"<wait.(.+?)>")
    REGEX_KEY = re.compile(r"KEY")

    @classmethod
    def check_modified_macros(cls):
        has_changed = False
        allfiles = os.listdir(cls.craft_folder)
        allfilepaths = [os.path.join(cls.craft_folder, fp) for fp in allfiles]
        current_mod_config = {k: os.path.getmtime(k) for k in allfilepaths}
        last_mod_config = cls.config["craft"]["last_modified"]
        macros_config = cls.config["craft"]["macros"]

        if current_mod_config != last_mod_config:
            printc.text("> Found new macro changes.", "yel")
            has_changed = True
            macros_config = {}

            for fp in allfilepaths:
                parsed_macro = cls._parse_update_macro(fp)
                macros_config[fp] = parsed_macro

        return has_changed, current_mod_config, macros_config, allfiles

    @classmethod
    def adjust_sleeps(cls):
        pass

    @classmethod
    def _parse_update_macro(cls, fp: str):
        macro = {"keys": [], "wait": []}
        key_idx = 0
        with open(fp, "r", encoding="utf8", errors="ignore") as f:
            for line in f.readlines():
                key, wait = CraftConfig.parse_macro_line(line)
                if key:
                    macro["keys"].append(key)
                    key_idx = len(macro["keys"]) - 1
                    macro["wait"].append(0)
                if wait:
                    macro["wait"][key_idx] += wait
        return macro

    @staticmethod
    def parse_macro_line(line):
        key, wait = None, None
        key_check = CraftConfig.REGEX_KEY.findall(line)
        wait_check = CraftConfig.REGEX_WAIT.findall(line)

        if key_check != []:
            key = line.split()[1]
        if wait_check != []:
            wait = int(wait_check[0])

        return key, wait


class Craft:
    def __init__(self):
        self.OPTIONS = {
            "--repair": Craft.repair,
            "--afk": None
        }

    def _estimate_time_completion(self, amt:int, config, macro) -> float:
        result = 0
        sleep_buffers = sum(list(config.config["craft"]["sleeps"].values()))
        step_sleep = sum(macro["wait"])
        result = amt * (sleep_buffers + step_sleep)
        print(result)
        return result / 60 # in minutes

    @staticmethod
    def repair(proc, count, buttons, opt_buttons):
        if count % int(opt_buttons["repair_threshold"]) == 0:
            print("> Repairing...", end="")
            sequence = [
                buttons["esc"],
                opt_buttons["repair"],
                buttons["left"],
                buttons["select"],
                buttons["left"],
                buttons["select"]
            ]
            for key in sequence:
                proc.press_key(key)
                sleep(0.5)
            sleep(4) # repair animation
            proc.press_key(opt_buttons["craft_item"]) # craft item button
            print("done.")

    def run(self, proc, config, macro_name: str, amt: Optional[int], opts: List):
        prestart = config.config["craft"]["sleeps"]["prestart"]
        poststep = config.config["craft"]["sleeps"]["poststep"]
        postfinish = config.config["craft"]["sleeps"]["postfinish"]

        buttons = config.buttons
        opt_buttons = config.config["craft"]["opt_buttons"]

        name = os.path.join(config.craft_folder, macro_name)
        macro = config.config["craft"]["macros"][name]

        count = 1
        run_opts = False

        if len(opts) > 0:
            run_opts = True
            print(f">>> Options selected: {opts}")

        if not amt:
            printc.text(f">>> Amount not specified, running until CTRL+C is pressed.", "yel")
        else:
            print(f">>> Amount specified: {amt} crafts.")
            est = self._estimate_time_completion(amt, config, macro)
            print(f">>> Estimated completion time: {est:.2f}m")

        print(f">>> Using macro: {name}")
        while True:
            try:
                if amt and count > amt:
                    printc.text(">> Crafts finished.", "gre")
                    break

                if run_opts == True:
                    for opt in opts:
                        self.OPTIONS[opt](proc, count, buttons, opt_buttons)

                print(f"> Craft #{count}")
                for _ in range(4):
                    proc.press_key(buttons["select"])
                sleep(prestart) # sleep prestart

                for step in range(len(macro["keys"])):
                    key, wait = macro["keys"][step], macro["wait"][step]
                    print(f">> Pressing {key}")
                    proc.press_key(key)
                    print(f">> Waiting {wait}s")
                    sleep(wait + poststep) # sleep + select padding
                count += 1
                sleep(postfinish) # sleep post craft finish
            except KeyboardInterrupt:
                print("> Stopping craft")
                break
