# FFXIV Jidou Crafter

Automating crafting in FFXIV with a small script that runs in the background until you want to cancel it. This means you can craft in FFXIV while doing other things on the same computer.

---

## Setup :wrench:

[Python for Windows Ver: 3.7.4 (64-bit)](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe) - 
[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
  - **Add Python PATH Checkbox**
  
### Setup Shortcut

Go to where you installed the github repo's folder in Windows and type `cmd` in search to go to the file path in terminal. A shortcut is shown in the pictures below:

![windows_step](../assets/windows0.png)
![windows_step](../assets/windows1.png)
![windows_step](../assets/windows2.png)
![windows_step](../assets/windows3.png)


Install required packages inside the file path with snippet below:

```
pip install -r requirements.txt
```

Setup the program's JSON file inside the file path with snippet below:

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

`limit` : Limits how many crafts you want to do.
`collectable` : Adds extra 0 key pushes for collectable success menu.
`foodbuff` : Automatically reapplies food when it drops.
`potbuff` : Automatically reapplies pot when it drops.
`notify` : Gives you a Window's notification when craft is completed.

## Usage

```
python ffxiv_jidoucraft.py
python ffxiv_jidoucraft.py collectable
python ffxiv_jidoucraft.py collectable limit
python ffxiv_jidoucraft.py foodbuff
python ffxiv_jidoucraft.py potbuff notify
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
