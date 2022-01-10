#!/usr/bin/env python3
from exceptions.key_exceptions import NotSameLengthException
from pydantic import BaseModel, root_validator
from typing import List

class SingleArgsKey:
    """Single craft arg commands, for len of 1 args"""
    pass

class MainArgsKey(BaseModel):
    """Main key args container"""
    keys: List[str]
    intervals: List[float]

    @root_validator
    def check_same_lengths(cls, values):
        if len(values.get("keys")) != len(values.get("intervals")):
            raise NotSameLengthException(values)
        return values
