#!/usr/bin/env python3
"""Models for identifying and containing craft args"""
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict


class SingleArgsCraft(Enum):
    """Single craft arg commands, for len of 1 commands."""
    listm = "list"

class OptArgsCraft(Enum):
    """Optional craft arg commands"""
    repair = "repair"
    afk = "afk"
    food = "food"
    pot = "pot"

class MainArgsCraft(BaseModel):
    """Main craft args container"""
    macro: Optional[Dict] = None
    macros_dict: Optional[Dict] = None
    macro_name: Optional[str] = None
    macro_file: Optional[str] = None
    amt: int = 0
    pot_count: int = 0
    food_count: int = 0
    single: Optional[SingleArgsCraft] = None
    opts: Optional[List[OptArgsCraft]] = None

if __name__ == "__main__":
    print(type(OptArgsCraft.repair))
