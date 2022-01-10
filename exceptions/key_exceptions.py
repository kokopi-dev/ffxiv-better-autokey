#!/usr/bin/env python3

class NotSameLengthException(Exception):
    """For multi key and intervals, length of each need to be the same"""
    def __init__(self, values):
        self.values = values
        self.message = "Amount of keys and intervals need to be the same."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.values} -> {self.message}"
