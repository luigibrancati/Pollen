## Pollen

Pollen register to monitor pollens.

### How to run the Python project

This project has been developed using [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

#### How to configure a python virtual environment using conda

Install Miniconda on your pc following the link provided above.

After the installation is done, you should be able to run `conda` from your terminal:
```bash
conda env list
```
On windows, you should now have the Anaconda Powershell Prompt, look for it in the search bar and ope it.

To create a new python virtual environment with Python 3.9.0 (the version used to develop this application):
```bash
conda create -n <env_name> python==3.9
```
After creating the environment, activate it
```bash
conda activate <env_name>
```
You should see the name of the environment in your terminal.

#### Install dependencies to run the package

You can now install the dependencies of this application by running
```bash
pip install -U -r requirements.txt
```
either in your newly created environment or on your base Python installation.

### How to build the EXE for Windows

To build the executable to be run on Windows (10 and above), you must be on Windows. Open a terminal inside the root folder of the repository and run:

```
pyinstaller.exe -c -w -i .\icons\pollen.ico --onefile -n Pollen main.py
```

By default, the executable `Pollen.exe` will be built inside the `./dist` folder. It can be distributed as it is.

### To do

Further improvements:
- Manage where to place logs and data; as of now, the app will just create `.logs` and `data` folders in its local folder;
- Add a button/functionality to redefine binding according to a user liking;
- Add button/functionality to add a pollen to the standard one, i.e. the ones shown by the app when it starts;
- Add Undo/Redo func (using a stack to save).
