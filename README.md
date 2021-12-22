# FFXIV Better Autokey

For all your background afking needs. Put FFXIV on a submonitor and afk while doing something else.

---

## Caveats
In order to be fully automatic while doing other things in the background, **FFXIV needs to be in windowed mode on your display #2**

![ffxivauto2](../assets/ffxivauto2.PNG)

![ffxivauto1](../assets/ffxivauto1.png)

---

## Setup

Currently for Windows only due to background keystroke working for win32

- Python LATEST recommended: 3.8+ (https://www.python.org/downloads/windows/)
- Manage Python Versions On Windows Reference: (https://changhsinlee.com/windows-py-launcher/)

### Check PATH during installation
![path_check](../assets/pythonpathcheck.PNG)

---

## How To Run

Run/double-click `cmd.bat`

---

## Commands

### Key
Description: `key [KEY] [INTERVAL]`

Primarily for afking or background afking

Example:

```
# Press c for opening and closing character menu every 60.5 seconds
(BetterAutoKey) key c 60.5
Interval: [60.5] in secs
> Pressing c <wait.(60.5)>
...

# Map each key to a specific interval
(BetterAutoKey) key 1,2 2.5,3
Interval: [2.5, 3.0] in secs
> Pressing 1 <wait.(2.5)>
> Pressing 2 <wait.(3.0)>
```

### Craft
Description: `craft [OPT:list] [macro] [OPT:amt] [OPT:--repair]`

Background automated crafting

**Adding/Deleting macros**:
  - Make a new **one** word file to `macros/` folder with the example template below:

```
KEY 1
/ac Reflect <wait.3>
/ac Manipulation <wait.2>
/ac "Waste Not" <wait.2>
/ac Innovation <wait.2>

KEY 2
/ac "Preparatory Touch" <wait.3>
/ac "Preparatory Touch" <wait.3>
/ac "Groundwork" <wait.3>
```

Command Examples:
```
(BetterAutoKey) craft list
['4star.txt', 'dura40.txt', 'test.txt']

(BetterAutoKey) craft dura40
>>> Press CTRL+C to quit.
>>> Options selected: ['--repair']
>>> Amount specified: 2 crafts.
>>> Using macro: macros\dura40.txt
...

(BetterAutoKey) craft dura40 12
>>> Press CTRL+C to quit.
>>> Amount specified: 2 crafts.
>>> Using macro: macros\dura40.txt
...

(BetterAutoKey) craft dura40 12 --repair
>>> Press CTRL+C to quit.
>>> Using macro: macros\dura40.txt
...
```

### Config

#### Adjusting `sleeps` Timers:
There are 3 sleep steps during a craft:
  - `prestart`: Sleep after selecting the Synthesize button, before starting the craft
  - `poststep`: Sleep added to after final <wait> due to speed of next key press
  - `postfinish`: Sleep added after finishing the craft due to speed of next key press

Examples:
```
(BetterAutoKey) config sleeps prestart 1.5
> Config set: prestart to 1.5.
> Wrote new config to .craft_config.json.
```

#### Adjusting `buttons`:
 - `repair`: The key for your repair menu (default is hotbar key '4')
 - `craft_item`: The key for the item you are crafting (default is hotbar key '5')

Examples:
```
(BetterAutoKey) config buttons repair 2
...
(BetterAutoKey) config buttons craft_item 3
...
```

#### Adjusting `repair` Settings:
 - `threshold` Repair has a threshold setting for how many crafts finished before starting to repair

 Examples:
 ```
 (BetterAutoKey) config repair threshold 91
 ...
 ```
