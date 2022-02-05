## Pollen

Pollen register to monitor pollens.

### How to build the EXE for Windows

To build the executable to be run on Windows (10 and above), you must be on Windows. Open a terminal inside the root folder of the repository and run:

```
pyinstaller.exe -c -w -i .\icons\pollen.ico --onefile -n Pollen main.py
```

By default, the EXE will be built inside the `./dist` folder. It can be distributed as it is.

### To do

Further improvements:
- Manage where to place logs and data; as of now, the app will just create `.logs` and `data` folders in its local folder;
- Add a button/functionality to redefine binding according to a user liking;
- Add button/functionality to add a pollen to the standard one, i.e. the ones shown by the app when it starts;
- Add Undo/Redo func (using a stack to save).