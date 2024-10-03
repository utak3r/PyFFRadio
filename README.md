# PyFFRadio

Simple app for playing internet radio.  
It relies on a simple INI file with radio stations names, stream urls and logo urls. See the included sample INI file.
No editor at this point.  
It is using the simplest version of PySimpleGui, as I wanted to check what's possible with that lib.  
For actual stream playback it's utilizing ffplay. Path to directory containing it is stored in an INI file.

![Screenshot](./screenshot.png?raw=true "Screenshot of a running application")


# Prerequisites
- Python >= 3.11
- PySimpleGui
- requests
- Pillow
- base64
- asyncio
- ConfigParser
- PyInstaller (not for running, but for building independent standalone executable)

# Running
Run this little app::
```
python -m PyFFRadio
```

Some useful things for easy VSCode usage are included, in *launch.json*, *settings.json* and *tasks.json*.  
Also *PyFFRadio.spec* file for using with PyInstaller is included.

# Building a standalone app without Python
Just run PyInstaller using included spec file:
```
pyinstaller --clean PyFFRadio.spec
```
