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
        "repair": "4",
        "repair_threshold": 90,
        "craft_item": "5"
    }
}
