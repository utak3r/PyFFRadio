# PyFFRadio

Simple app for playing internet radio.
Just started the skeleton, so not so much in here yet.
Stay tuned! ;)

**Edit**

It's slowly progressing. See the below screenshot.
![Screenshot](./screenshot.png?raw=true "Screenshot of a running application")

# Running
Run this little app::
```
python -m PyFFRadio
```

For VSCode, use *launch.json* file in your *.vscode* subdirectory:
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Module",
            "type": "debugpy",
            "request": "launch",
            "module": "PyFFRadio"
        }
    ]
}
```

# Building a standalone app without Python
Just run PyInstaller using included spec file:
```
pyinstaller --clean PyFFRadio.spec
```
