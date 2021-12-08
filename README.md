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
Description: `craft [macro] [OPT:amt]`

Background automated crafting
