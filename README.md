# FFXIV Jidou Crafter

Automating crafting in FFXIV with a small script that runs in the background until you want to cancel it. This means you can craft in FFXIV while doing other things on the same computer.

---

## Setup :wrench:

[Python for Windows Ver: 3.7.4 (64-bit)](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exehttps://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe)
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

**Finding `process_name`**

![finding_process](../assets/detailpid.png)

**Calculating wait times for corresponding macro:**

![adding_wait_example](../assets/macro.jpg)

---

## Usage :computer:
**Executing the program:**
**1. Make sure your crafting window is active, and that you've selected the item to craft.**
![highlighted_item_craft_window](../assets/window.jpg)

2. Open up the terminal and navigate to the script `ffxiv_jidoucraft.py`
3. Enter the command `python ffxiv_jidoucraft.py`
4. Press Ctrl+C when you want to end the script

![stopping program](../assets/stopped.jpg)

---

## Commands

```
python ffxiv_jidoucraft.py
python ffxiv_jidoucraft.py collectable
python ffxiv_jidoucraft.py foodbuff
python ffxiv_jidoucraft.py potbuff
python ffxiv_jidoucraft.py foodbuff potbuff
python ffxiv_jidoucraft.py foodbuff potbuff collectable
```

## Json Editor

```
python json_editor.py
```

Follow instructions in the script messages.

---

## Author
* **Derrick Gee** - [kai-dg](https://github.com/kai-dg)
