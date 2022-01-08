#!/usr/bin/env python3
"""Handling all process related info"""
import re
import psutil
from pywinauto.application import Application
from pywinauto.keyboard import *
from utils.tty_colors import PrintColor as printc
from utils.tty_colors import Colors
from typing import Optional, List
from pydantic import BaseModel
import sys
PROCESS_TARGET = "ffxiv_dx11.exe"
WINDOW_TITLE = "FINAL FANTASY XIV"
# PROCESS_TARGET = "notepad.exe"
# WINDOW_TITLE = "Notepad - Untitled"


class PID(BaseModel):
    name: str
    id: int

class Process:
    """Gets PID of PROCESS_TARGET, then hooks onto the PID on init.
    Also contains key press sequences.
    """
    pid: Optional[PID]
    app: Application
    all_pids: List[PID] = []
    connected_apps: List[Application] = []

    def __init__(self):
        self.pid = self.find_pid()
        self.app = self.connect_to_pid(self.pid)

    def find_pid(self):
        """Finds and adds to list of PIDs. Returns last found PID"""
        pid = None
        for p in psutil.process_iter():
            try:
                if p.name() == PROCESS_TARGET:
                    query = re.search("pid=(.+?), name=", str(p))
                    if query:
                        pid_id = int(query.group(1))
                        pid = PID(id=pid_id, name=f"FFXIV #{len(self.all_pids)}")
                        self.all_pids.append(pid)
                        printc.text(f"> Found FFXIV PID: {pid}", Colors.GRE)
            except psutil.AccessDenied:
                # Psutil cannot read system processes like CPU, so need this exception
                pass
        return pid

    def connect_to_pid(self, pid: PID = None):
        """Returns a pywinauto Application object created with find_pid()"""
        if pid:
            try:
                app = Application().connect(process=pid.id)
                self.connected_apps.append(app)
                printc.text(f"> Connected {pid} success", Colors.GRE)
                printc.text(f"> Added {pid} to connected apps", Colors.GRE)
                return app
            except Exception as e:
                printc.text(f"> Could not connect to {pid}", Colors.RED)
                printc.text(f"> {e}", Colors.RED)
        else:
            printc.text(f"ERROR: Could not find process name: {PROCESS_TARGET}", Colors.RED)
            printc.text(f"Try running this again when FFXIV is opened.", Colors.YEL)
            sys.exit()

        return None

    def press_key(self, key: str):
        """Presses a key. Refer to:
        https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
        """
        self.app.window(title=WINDOW_TITLE).send_keystrokes(key)
        
    def press_char(self, char: str):
        """Types out a char"""
        self.app.window(title=WINDOW_TITLE).send_chars(char)
