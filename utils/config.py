#!/usr/bin/env python3
"""
Config keys layout:
    config: {
        general: {},
        craft: {}
    }
"""
import os
import json
from utils import debug
from utils.craft import CraftConfig
from utils.tty_colors import PrintColor as printc


class BAKConfig(CraftConfig):
    config = {}
    # General Config
    general_filename = ".general_config.json"
    general_template = {"debug_status": False}
    buttons = { # Remapping of special keys
        "left": "{LEFT}",
        "right": "{RIGHT}",
        "esc": "{VK_ESCAPE}",
        "select": "{VK_NUMPAD0}",
    }

    # Craft Config
    craft_filename = ".craft_config.json"
    craft_template = {
        "last_modified": {},
        "macros": {},
        "macros_list": [],
        "sleeps": {
            "prestart": 2,
            "poststep": 1,
            "postfinish": 2
        },
        "opt_buttons": {
            "repair": "4",
            "repair_threshold": 90,
            "craft_item": "5"
        }
    }
    craft_folder = "macros"

    def __init__(self):
        self.general_config_init()
        self.craft_config_init()
        self.debug_check()
        printc.text("> Initialized configs...", "gre")

    def write_config(self, config_filename: str, config_type: str):
        """Writes to config_filename using self.config['config_type']
        Args:
            config_filename = attribute _filename ext
        """
        type_filename = getattr(self, config_filename, None)
        if not type_filename: #TODO create custom exceptions
            printc.text(f"ERROR: {type_filename} attr does not exist in {self.__class__}", "red")
            return

        with open(type_filename, "w+") as f:
            json.dump(self.config[config_type], f)
            printc.text(f"> Wrote new config to {type_filename}.", "gre")

    def _config_init(self, config_filename: str, template: str, config_type: str):
        """
        Args:
            config_filename = attribute _filename ext
            template = attribute _template ext
        """
        type_filename = getattr(self, config_filename, None)
        type_template = getattr(self, template, None)
        if not type_filename or not type_template: #TODO create custom exceptions
            printc.text(f"ERROR: {config_filename} or {template} attr does not exist in {self.__class__}", "red")
            return

        if not os.path.exists(type_filename):
            with open(type_filename, "w") as f:
                json.dump(type_template, f)
                self.config[config_type] = type_template
                printc.text(f"> Created new config file: {type_filename}", "gre")
        else:
            with open(type_filename, "r") as f:
                self.config[config_type] = json.load(f)

    # def config_nested_keys_set(self, keys, value):
        # temp = {}
        # for key in keys:
            # if self.config.get(key, None):
                # temp = self.config.get(key)
        # if temp and temp != {}:
            # temp[keys[-1]] = value # pointing to config
            # print(f"> Config set: {keys[-1]} to {value}.")

    def general_config_init(self):
        self._config_init("general_filename", "general_template", "general")

    def craft_config_init(self):
        self._config_init("craft_filename", "craft_template", "craft")
        if not os.path.exists(self.craft_folder):
            os.mkdir(self.craft_folder)
            printc.text("> Created new folder: macros/", "gre")

    def debug_check(self):
        """Run debug command for win32 error"""
        if self.config["general"]["debug_status"] == False:
            debug.setupme()
            self.config["general"]["debug_status"] = True
            self.write_config("general_filename", "general")
