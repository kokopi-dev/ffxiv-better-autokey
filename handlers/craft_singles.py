#!/usr/bin/env python3
from pydantic import BaseModel
from typing import Dict, Callable

def craft_list(macro_dict: Dict):
    print(f"{macro_dict}")

class CraftSinglesCommands(BaseModel):
    listm: Callable

CraftSinglesHandler = CraftSinglesCommands(
    listm = craft_list
)
