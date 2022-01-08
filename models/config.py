#!/usr/bin/env python3
from pydantic import BaseModel


class CraftSleeps(BaseModel):
    """sleep() timings for before starting the craft, before selecting a step,
    and after finishing a craft.
    """
    prestart: int = 2
    poststep: int = 1
    postfinish: int = 2
