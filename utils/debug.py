#!/usr/bin/env python3
"""For debugging the win32 error that occurs for pywinauto"""
import requests
import os
import sys


def update_requirements(old_mod_time, new_mod_time):
    """Checks if there has been updates the requirements.txt, updates if
    there is a change in modified file time against the recorded"""
    if old_mod_time != new_mod_time:
        os.system("python -m pip install -r requirements.txt")
        print("> Just installed new dependency updates, please restart the program.")
        return True
    return False

def setupme():
    print("> Checking pip:")
    os.system("python -m pip install --upgrade pip")

    default_link = "https://github.com/CristiFati/Prebuilt-Binaries/raw/master/PyWin32/v228/pywin32-228-cp39-cp39-win_amd64.whl"
    print(f"> Downloading from {default_link}")
    r = requests.get(default_link)

    filename = default_link.split("/")[-1]
    with open(filename, "wb") as f:
        f.write(r.content)
        print(f"> Wrote new file: {filename}")

    print(f"> Running pywin32 fix:")
    os.system(f"python -m pip install -U --force-reinstall {filename}")

    print(f"> Trying to delete {filename}...")
    os.remove(filename)
    print(f"> Deleted {filename}...")

if __name__ == "__main__":
    setupme()
