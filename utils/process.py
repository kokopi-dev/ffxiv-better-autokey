#!/usr/bin/env python3
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *
PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"


class Process:
    """Gets PID of PROCESS_TARGET, then hooks onto the PID on init.
    Also contains key press sequences.
    """
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
        print(f"> Found FFXIV PID: {pid}")
        return pid

    def connect_to_pid(self):
        """Returns a pywinauto Application object created with find_pid()"""
        if not self.pid:
            return f"ERROR: Could not find process name: {PROCESS_TARGET}."
        app = Application().connect(process=self.pid)
        print("> Connected to FFXIV PID")
        return app

    def press_key(self, key: str):
        """Presses a key. Refer to:
        https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
        """
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)
        
    def press_char(self, char: str):
        """Types out a char"""
        self.app.window(title=WINDOW_TITLE).send_chars(char)
