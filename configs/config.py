#!/usr/bin/env python3
"""Mostly constant variables"""
from configs.craft_config import CraftConfig
from configs.general_config import GeneralConfig
from pydantic import BaseModel

class Buttons(BaseModel):
    """Remapping of special keys"""
    left: str = "{LEFT}"
    right: str = "{RIGHT}"
    up: str = "{UP}"
    down: str = "{DOWN}"
    esc: str = "{VK_ESCAPE}"
    select: str = "{VK_NUMPAD0}"
    submenu: str = "'"

class Config:
    craft: CraftConfig
    general: GeneralConfig

    buttons: Buttons = Buttons()

    def __init__(self):
        self.craft = CraftConfig()
        self.general = GeneralConfig()
