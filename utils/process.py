#!/usr/bin/env python3
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *
PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"

class Process:
    """Gets PID, then hooks onto the PID to be able to send keystrokes to"""
    def __init__(self):
        self.pid = self.find_pid()
        self.app = self.connect_to_pid()

    def find_pid(self):
        pid = None
        for p in psutil.process_iter():
            try:
                if p.name() == PROCESS_TARGET:
                    query = re.search("pid=(.+?), name=", str(p))
                    pid = int(query.group(1))
            except psutil.AccessDenied:
                # Psutil cannot read system processes like CPU, so need this exception
                pass
        return pid

    def connect_to_pid(self):
        if not self.pid:
            print(f"ERROR: Could not find process name: {PROCESS_TARGET}.")
            quit()
        app = Application().connect(process=self.pid)
        return app

    def press_key(self, key: str):
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)