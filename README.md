# FFXIV Jidou Crafter

---

## Setup :wrench:

[Python Ver: 3.7.4 (64-bit)](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exehttps://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe)
  - **Add Python PATH**

Install required packages with snippet below:

```
pip install -r requirements.txt
```

Setup the program's JSON file with snippet below:

```
python setup.py
```

---

## Description

Automating crafting in FFXIV with a small script that runs in the background until you want to cancel it. This means you can craft in FFXIV while doing other things on the same computer.

## Instructions

* **Install required things above**

**Make sure your ffxiv process is this name:**
* If it is incorrect, you can change it via command `editprocess`
* Go to `task manager->right click FFXIV's process->go to details` to find the process name

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
* `python ffxiv-autocraft.py editprocess` : allows you to edit process name, incase you are not using dx11
* `python ffxiv-autocraft.py autobuff` : check below for instructions
* CTRL+C will quit the program, make sure you get the message `Program has stopped.` to know that it stopped

---

## Autobuff Feature

* Cannot use food time extending buffs (will implement later)
* Default: Make sure your macro 1 is on key 1, macro 2 is on key 2, pot buff is on key 3, food buff is on key 4, and crafting item is on key 5. Image example below
* Make sure your keys and macro timers are correct
* Running this command will prompt you to enter your current buff timers for both food and pot

![autobuff bar](../assets/autobuff.png)

---

## Author
* **Derrick Gee** - [kai-dg](https://github.com/kai-dg)
