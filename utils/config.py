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


class BAKConfig:
    config = {}
    # General Config
    general_filename = ".general_config.json"
    general_template = {"debug_status": False}
    buttons = { # Remapping of special keys
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

    def _config_init(self, config_filename: str, template: str, config_type: str):
        """config_filename = attribute _filename ext
        template = attribute _template ext
        """
        type_filename = getattr(self, config_filename, None)
        type_template = getattr(self, template, None)
        if not type_filename or type_template: #TODO create custom exceptions
            print(f"ERROR: {type_filename} attr does not exist in {self.__class__}")
            return

        if not os.path.exists(type_filename):
            with open(self.general_filename, "w") as f:
                json.dump(type_template, f)
                print(f"> Created new config file: {self.general_filename}")
        else:
            with open(type_filename, "r") as f:
                self.config[config_type] = json.load(f)


    def general_config_init(self):
        self._config_init("general_filename", "general_template", "general")

    def craft_config_init(self):
        self._config_init("craft_filename", "craft_template", "craft")

    def debug_check(self):
        """Run debug command for win32 error"""
        if self.config["debug_status"] == False:
            pass

