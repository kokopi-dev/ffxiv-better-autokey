#!/usr/bin/env python3
import os
import json
TEMPLATE = {"debug_status": False}


class BAKConfig:
    filename = ".config.json"
    debug_status = False
    buttons = { # Remapping of special keys
        "left": "{LEFT}",
        "right": "{RIGHT}",
        "ESC": "{VK_ESCAPE}",
        "SELECT": "{VK_NUMPAD0}",
    }
    config = {}

    def __init__(self):
        self.config_init()
        self.debug_check()

    def config_init(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump(TEMPLATE, f)
        else:
            with open(self.filename, "r") as f:
                self.config = json.load(f)

    def debug_check(self):
        self.debug_status = self.config["debug_status"]
