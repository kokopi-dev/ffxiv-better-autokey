# Automating FFXIV Crafting

---

## Required things

* (get python 3)
* pip install -U pywinauto
* pip install psutil

---

## Description

Automating crafting in FFXIV with a small script that runs in the background until you want to cancel it. This means you can craft in FFXIV while doing other things on the same computer.

## Instructions

* **Install required things above**

**Make sure your ffxiv process is this name:**
* If it is incorrect, change `process_name` variable in ffxiv-autocraft.py

![finding_process](../assets/detailpid.png)

**Calculating wait times for corresponding macro:**

![adding_wait_example](../assets/macro.jpg)

**Executing the program:**
**1. Make sure your crafting window is active, and that you've selected the item to craft.**
![highlighted_item_craft_window](../assets/window.jpg)

2. Open up the terminal and navigate to the program `auto-craft.py`
3. Enter the command `python auto-craft.py`
4. Press Ctrl+C when you want to end the script
  - Make sure you see the program stopped message to make sure you've exited the program
![stopping program](../assets/stopped.jpg)

---

## All Commands

* `python ffxiv-autocraft.py` : runs the autocrafter with current timer settings
* `python ffxiv-autocraft.py edit` : allows you to edit timers one by one, follow prompt messages
* `python ffxiv-autocraft.py editkeys` : allows you to edit keystrokes one by one, follow prompt messages
* CTRL+C will quit the program, make sure you get the message `Program has stopped.` to know that it stopped

---

## Author
* **Derrick Gee** - [kai-dg](https://github.com/kai-dg)
