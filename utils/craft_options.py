#!/usr/bin/env python3
from pydantic import BaseModel
from typing import Callable
from time import sleep
from utils.process import Process

class CraftOptRunArgs(BaseModel):
    proc: Process
    craft_count: int
    class Config:
        arbitrary_types_allowed = True

# make buttons a constant
def repair(proc, count):
    from config import buttons, opt_buttons
    if count % int(opt_buttons.repair_threshold) == 0:
        print("> Repairing...", end="")
        sequence = [
            buttons.esc,
            opt_buttons.repair,
            buttons.left,
            buttons.select,
            buttons.left,
            buttons.select
        ]
        for key in sequence:
            proc.press_key(key)
            sleep(0.5)
        sleep(4) # repair animation
        proc.press_key(opt_buttons.craft_item) # craft item button
        print("done.")

def afk(proc, count, buttons, opt_buttons):
    """Afk function happens in auto.py after craft finishes"""
    pass

def pot():
    pass

def food():
    pass

class CraftOptions(BaseModel):
    repair: Callable
    afk: Callable
    food: Callable
    pot: Callable

CraftOpts = CraftOptions(
    repair=repair,
    afk=afk,
    pot=pot,
    food=food
)
