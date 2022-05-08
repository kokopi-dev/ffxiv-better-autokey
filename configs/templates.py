#!/usr/bin/env python3
from pathlib import Path

general = {
    "debug_status": False,
    "requirements": Path("requirements.txt").stat().st_mtime
}
craft = {
    "last_modified": {},
    "macros": {},
    "sleeps": {
        "prestart": 2,
        "poststep": 1,
        "postfinish": 2
    },
    "opt_buttons": {
        "repair": "3",
        "repair_threshold": 100,
        "item": "4",
        "food": "5",
        "pot": "6"
    },
    "repair": {
        "cursor_delay": 0.6,
        "animation_wait": 5,
        "craft_menu_wait": 2
    }
}
