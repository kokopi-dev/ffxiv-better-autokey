# Automating FFXIV Crafting

---

## Required things

* (get python 3)
* pip install -U pywinauto

---

## Description

Automating crafting in FFXIV with a small script that runs in the background until you want to cancel it. This means you can craft in FFXIV while doing other things on the same computer.

## Instructions

* **Install required things above**

**Setting correct PID in auto-craft:**
![finding_PID](../assets/pid.jpg)

**Setting up sleep times after each macro:**

![adding_wait_example](../assets/macro.jpg)

**Executing the program:**
1. Make sure your crafting window is active, and that you've selected the item to craft.
![highlighted_item_craft_window](../assets/window.jpg)

2. Open up the terminal and navigate to the program `auto-py`
3. Enter the command `python auto-craft.py`
4. Press Ctrl+C when you want to end the script
