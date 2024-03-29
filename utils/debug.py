#!/usr/bin/env python3
"""For debugging the win32 error that occurs for pywinauto"""
import requests
import os


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
