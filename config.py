#!/usr/bin/env python3
import os
import json
from utils import debug
from utils.tty_colors import PrintColor as printc
import re
from utils.tty_colors import Colors
from pydantic import BaseModel
from typing import Dict, List
from utils.macro import parse_update_macro, parse_macro_line
conf = None
buttons = None
opt_buttons = None
craft_sleeps = None
macros_conf = None


class OptButtons(BaseModel):
    """User defined option button mappings"""
    repair: str = "4"
    repair_threshold: int = 90
    craft_item: str = "5"

class Buttons(BaseModel):
    """Remapping of special keys"""
    left: str = "{LEFT}"
    right: str = "{RIGHT}"
    up: str = "{UP}"
    down: str = "{DOWN}"
    esc: str = "{VK_ESCAPE}"
    select: str = "{VK_NUMPAD0}"
    submenu: str = "'"

class CraftSleeps(BaseModel):
    """sleep() timings for before starting the craft, before selecting a step,
    and after finishing a craft.
    """
    prestart: int = 2
    poststep: int = 1
    postfinish: int = 2
    def updateself(self):
        data = self.dict()
        conf.config["craft"]["sleeps"] = data
        conf.write_config("craft_filename", "craft")

class CraftMacros(BaseModel):
    all_macros: Dict
    last_mod: Dict
    macros_list: List

class Config:
    config = {}
    # General Config
    general_filename = ".general_config.json"
    general_template = {"debug_status": False}
    REGEX_WAIT = re.compile(r"<wait.(.+?)>")
    REGEX_KEY = re.compile(r"KEY")

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
        }
    }
    craft_folder = "macros"

    def __init__(self):
        self.general_config_init()
        self.craft_config_init()
        self.debug_check()
        printc.text("> Initialized configs...", Colors.GRE)

    def write_config(self, config_filename: str, config_type: str):
        """Writes to config_filename using self.config['config_type']
        Args:
            config_filename = attribute *_filename ext
        """
        type_filename = getattr(self, config_filename, None)
        if not type_filename: #TODO create custom exceptions
            printc.text(f"ERROR: {type_filename} attr does not exist in {self.__class__}", Colors.RED)
            return

        with open(type_filename, "w+") as f:
            json.dump(self.config[config_type], f)
            printc.text(f"> Wrote new config to {type_filename}.", Colors.GRE)

    def _config_init(self, config_filename: str, template: str, config_type: str):
        """
        Args:
            config_filename = attribute _filename ext
            template = attribute _template ext
        """
        type_filename = getattr(self, config_filename, None)
        type_template = getattr(self, template, None)
        if not type_filename or not type_template: #TODO create custom exceptions
            printc.text(f"ERROR: {config_filename} or {template} attr does not exist in {self.__class__}", Colors.RED)
            return

        if not os.path.exists(type_filename):
            with open(type_filename, "w") as f:
                json.dump(type_template, f)
                self.config[config_type] = type_template
                printc.text(f"> Created new config file: {type_filename}", Colors.GRE)
        else:
            with open(type_filename, "r") as f:
                self.config[config_type] = json.load(f)

    def general_config_init(self):
        self._config_init("general_filename", "general_template", "general")

    def craft_config_init(self):
        self._config_init("craft_filename", "craft_template", "craft")
        if not os.path.exists(self.craft_folder):
            os.mkdir(self.craft_folder)
            printc.text("> Created new folder: macros/", Colors.GRE)

    def debug_check(self):
        """Run debug command for win32 error"""
        if self.config["general"]["debug_status"] == False:
            debug.setupme()
            self.config["general"]["debug_status"] = True
            self.write_config("general_filename", "general")

    def check_modified_macros(self):
        has_changed = False
        allfiles = os.listdir(self.craft_folder)
        allfilepaths = [os.path.join(self.craft_folder, fp) for fp in allfiles]
        current_mod_config = {k: os.path.getmtime(k) for k in allfilepaths}
        last_mod_config = self.config["craft"]["last_modified"]
        macros_config = self.config["craft"]["macros"]

        if current_mod_config != last_mod_config:
            printc.text("> Found new macro changes.", Colors.YEL)
            has_changed = True
            macros_config = {}

            for fp in allfilepaths:
                parsed_macro = parse_update_macro(fp)
                macros_config[fp] = parsed_macro

        return has_changed, current_mod_config, macros_config, allfiles

conf = Config()
buttons = Buttons()
opt_buttons = OptButtons()

craft_sleeps = CraftSleeps(**conf.craft_template["sleeps"])
macros_conf = CraftMacros(
    all_macros = conf.craft_template["macros"],
    last_mod = conf.craft_template["last_modified"],
    macros_list = conf.craft_template["macros_list"]
)
