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
Description: `craft [OPT:list] [macro_name] [OPT:amt] [OPT:repair=true|afk=true|pot=0|food=0]`

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

(BetterAutoKey) craft dura35
>>> Press CTRL+C to quit.
>>> Amount not specified, running until CTRL+C is pressed.
>>> Using macro: dura40
...

(BetterAutoKey) craft dura35 12
>>> Press CTRL+C to quit.
>>> Amount specified: 12 crafts.
>>> Using macro: dura40
...

(BetterAutoKey) craft dura35 12 repair=true
>>> Press CTRL+C to quit.
> Options selected: repair
>>> Repair Key: 3
>>> Craft Item Key: 4
>>> Using macro: dura40
...

# food=15 means that you have 15 minutes remaining on your current food buff
(BetterAutoKey) craft dura35 12 food=15
>>> Press CTRL+C to quit.
> Options selected: food
>>> Repair Key: 3
>>> Craft Item Key: 4
>>> Using macro: dura40
...
```

### Config

#### Listing all config values:
```
(BetterAutoKey) config list
Craft Opt Settings: repair='3' repair_threshold=100 item='4' food='5' pot='6'
Craft Sleep Settings: prestart=2 poststep=1 postfinish=2
Craft Repair Settings: cursor_delay=0.6 animation_wait=5 craft_menu_wait=2
```

#### Refreshing config values to default:
```
(BetterAutoKey) config refresh
> Refreshing current config with default settings...
> Wrote new config to .craft_config.json.
```

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

---

### Development

Vim pyright environment access (no pywinauto intellisense, but better than nothing):
- Linux venv: `. ./run linux`
  - `pip install -r linux_requirements.txt`
