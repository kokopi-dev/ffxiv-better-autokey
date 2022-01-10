#!/usr/bin/env python3
from pathlib import Path
from utils import debug
import json
from configs import templates
import sys

class GeneralConfig:
    filename: Path = Path(".general_config.json")

    debug_status: bool

    def __init__(self):
        config = None
        if not self.filename.exists():
            with open(self.filename, "w") as f:
                json.dump(templates.general, f)
                config = templates.general
        else:
            with open(self.filename, "r") as f:
                config = json.load(f)

        self.debug_status = config["debug_status"]

    def _getdict(self):
        return {
            "debug_status": self.debug_status
        }

    def write_config(self):
        config = self._getdict()
        with open(self.filename, "w") as f:
            json.dump(config, f)

    def debug_check(self):
        """Run debug command for win32 error"""
        if self.debug_status == False:
            debug.setupme()
            self.debug_status = True
            self.write_config()
            print("Installed proper pywin32 dependencies, please restart the program")
            sys.exit(1)
