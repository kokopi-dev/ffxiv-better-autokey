#!/usr/bin/env python3
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List
from configs import templates, regexes
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
import json


class MacrosHelper:
    """Namespace for macro helper"""

    @staticmethod
    def _parse_macro_line(line):
        key, wait = None, None
        key_check = regexes.key.findall(line)
        wait_check = regexes.wait.findall(line)

        if key_check != []:
            key = line.split()[1]
        if wait_check != []:
            wait = int(wait_check[0])

        return key, wait

    @staticmethod
    def parse_macro(filepath: Path):
        macro = {"keys": [], "wait": []}
        key_idx = 0
        with open(filepath, "r", encoding="utf8", errors="ignore") as f:
            for line in f.readlines():
                key, wait = MacrosHelper._parse_macro_line(line)
                if key:
                    macro["keys"].append(key)
                    key_idx = len(macro["keys"]) - 1
                    macro["wait"].append(0)
                if wait:
                    macro["wait"][key_idx] += wait
        return macro

class CraftOptButtons(BaseModel):
    """User defined option button mappings"""
    repair: str = "3"
    repair_threshold: int = 90
    item: str = "4"
    food: str = "5"
    pot: str = "6"

class CraftSleeps(BaseModel):
    """sleep() timings for before starting the craft, before selecting a step,
    and after finishing a craft.
    """
    prestart: int = 2
    poststep: int = 1
    postfinish: int = 2

class CraftMacros(BaseModel):
    macros: Dict
    last_modified: Dict

class CraftConfig:
    filename: Path = Path(".craft_config.json")
    folder: Path = Path("macros")

    macros: CraftMacros
    sleeps: CraftSleeps
    opt_buttons: CraftOptButtons

    def __init__(self):
        if not self.folder.is_dir():
            self.folder.mkdir(parents=True, exist_ok=True)

        config = None
        if not self.filename.exists():
            with open(self.filename, "w") as f:
                json.dump(templates.craft, f)
                config = templates.craft
        else:
            with open(self.filename, "r") as f:
                config = json.load(f)
        
        self.macros = CraftMacros(**{
            "macros": config["macros"],
            "last_modified": config["last_modified"]
        })
        self.sleeps = CraftSleeps(**config["sleeps"])
        self.opt_buttons = CraftOptButtons(**config["opt_buttons"])

    def _getdict(self):
        result = {}
        result.update(**self.macros.dict())
        result.update({"sleeps": self.sleeps.dict()})
        result.update({"opt_buttons": self.opt_buttons.dict()})
        return result

    def write_config(self):
        new_config = self._getdict()
        with open(self.filename, "w+") as f:
            json.dump(new_config, f)
            printc.text(f"> Wrote new config to {self.filename}.", Colors.GRE)

    def check_modified_macros(self):
        """Checks for new or modified macros, and updates+writes them"""
        allfiles = [i for i in self.folder.glob("*.txt")]
        current_mod_times = {str(i): i.stat().st_mtime for i in allfiles}
        last_mod_times = {**self.macros.last_modified}

        if current_mod_times != last_mod_times:
            printc.text("> Found new macro changes.", Colors.YEL)
            # very nice naive approach time
            for fp in allfiles:
                new_times = MacrosHelper.parse_macro(fp)
                self.macros.macros[str(fp.name)] = new_times
            self.macros.last_modified = current_mod_times
            self.write_config()
