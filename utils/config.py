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


class BAKConfig:
    config = {}
    # General Config
    general_filename = ".general_config.json"
    general_template = {"debug_status": False}
    buttons_remap = { # Remapping of special keys
        "left": "{LEFT}",
        "right": "{RIGHT}",
        "ESC": "{VK_ESCAPE}",
        "SELECT": "{VK_NUMPAD0}",
    }

    # Craft Config
    craft_filename = ".craft_config.json"
    craft_template = {"last_modified": {}, "macros": []}
    craft_folder = "macros"

    def __init__(self):
        self.general_config_init()
        self.craft_config_init()
        self.debug_check()

    def _write_config(self, config_filename: str, config_type: str):
        """Writes to config_filename using self.config['config_type']
        Args:
            config_filename = attribute _filename ext
        """
        type_filename = getattr(self, config_filename, None)
        if not type_filename: #TODO create custom exceptions
            print(f"ERROR: {type_filename} attr does not exist in {self.__class__}")
            return

        with open(type_filename, "w+") as f:
            json.dump(self.config[config_type], f)
            print(f"> Wrote new config to {type_filename}.")

    def _config_init(self, config_filename: str, template: str, config_type: str):
        """
        Args:
            config_filename = attribute _filename ext
            template = attribute _template ext
        """
        type_filename = getattr(self, config_filename, None)
        type_template = getattr(self, template, None)
        if not type_filename or not type_template: #TODO create custom exceptions
            print(f"ERROR: {config_filename} or {template} attr does not exist in {self.__class__}")
            return

        if not os.path.exists(type_filename):
            with open(type_filename, "w") as f:
                json.dump(type_template, f)
                self.config[config_type] = type_template
                print(f"> Created new config file: {type_filename}")
        else:
            with open(type_filename, "r") as f:
                self.config[config_type] = json.load(f)

    def general_config_init(self):
        self._config_init("general_filename", "general_template", "general")

    def craft_config_init(self):
        self._config_init("craft_filename", "craft_template", "craft")

    def debug_check(self):
        """Run debug command for win32 error"""
        if self.config["general"]["debug_status"] == False:
            debug.setupme()
            self.config["general"]["debug_status"] = True
            self._write_config("general_filename", "general")
