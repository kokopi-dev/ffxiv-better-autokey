#!/usr/bin/env python3
import datetime

def ts():
    return datetime.datetime.now().isoformat().split("T")[1]
