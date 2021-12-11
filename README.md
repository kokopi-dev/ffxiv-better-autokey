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
# Press c for opening and closing character menu every 60 seconds
(BetterAutoKey) key c 60
```

### Craft
Description: `craft [OPT:list] [macro] [OPT:amt]`

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

**Adjusting Sleep Timers**:
There are 3 sleep steps during a craft:
  - `prestart`: Sleep after selecting the Synthesize button, before starting the craft
  - `poststep`: Sleep added to after final <wait> due to speed of next key press
  - `postfinish`: Sleep added after finishing the craft due to speed of next key press
