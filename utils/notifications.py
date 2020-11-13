#!/usr/bin/env python3
import winsound
import sys
from time import sleep


def finished():
    if "win" in sys.platform:
        winsound.PlaySound("audio\\finished.wav", winsound.SND_ASYNC)
        sleep(3)
        sys.exit()
    else:
        print("Error: Notification is only for Windows.")
