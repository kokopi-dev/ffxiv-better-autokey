#!/usr/bin/env python3
"""Models for identifying and containing craft args"""
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict


class ConfigLocation(Enum):
    craft = "craft"
    general = "general"

class SingleArgsConfig(Enum):
    """Single craft arg commands, for len of 1 commands."""
    listm = "list"

class OptArgsConfig(Enum):
    buttons = "buttons"
    sleeps = "sleeps"

class MainArgsConfig(BaseModel):
    """Main craft args container"""
    location: Optional[ConfigLocation] = None
    key: Optional[str] = None
    value: Optional[str] = None
    single: Optional[SingleArgsConfig] = None
    opt: Optional[OptArgsConfig] = None
