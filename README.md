## Pollen

Pollen register to monitor pollens.

[![Pollen - Windows](https://github.com/luigibrancati/Pollen/actions/workflows/build.yml/badge.svg)](https://github.com/luigibrancati/Pollen/actions/workflows/build.yml)

### How to build the EXE for Windows

To build the executable to be run on Windows (10 and above), you must be on Windows. Open a terminal inside the root folder of the repository and run:

```
pyinstaller.exe -c -w -i .\icons\pollen.ico --onefile -n Pollen main.py
```

By default, the executable `Pollen.exe` will be built inside the `./dist` folder. It can be distributed as it is.
