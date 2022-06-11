from collections import deque
from tokenize import String
from config import _TLW_HEIGHT, _TLW_WIDTH
from pollen_class import Pollen
from tkinter import END, Toplevel, ttk, StringVar, Tk, filedialog, Text
from typing import TypeVar, Union
import pandas as pd
import os
import logging
from abc import ABC, abstractmethod


custom_logger = logging.getLogger(name="pollen_logger")
PF = TypeVar("PF", bound="PollenFrame")


# Pollen class is used both as a pollen representation and a tkinter frame
class PollenFrame(ttk.Frame):
    """Class to manage different pollen types.
    This class contains data about the pollen family, name and count.
    It also manages the frame to represent the pollen family
    and its key binding.
    """

    def __init__(self, master: ttk.Frame, fam: str, nome: str, count: int = 0) -> None:
        # Initialize the ttk.Frame class with a master frame
        super().__init__(master)
        self.master = master
        self.pollen = Pollen(fam, nome, count)
        # Stacks for the undo/redo functionality
        # These stacks store the previous states of the Pollen inside this PollenFrame
        # These are used to revert the state of the PollenFrame
        self.undo_stack = deque()
        self.redo_stack = deque()
        # Tkinter labels to show relevant info
        self.label_binding = ttk.Label(self, style="BindKey.TLabel")
        self.label_binding.grid(column=0, row=0, padx=5)
        self.label = ttk.Label(self, style="Generic.TLabel")
        self.label.grid(column=1, row=0, padx=5)
        # Create a string variable using tkinter class StringVar
        self.contents = StringVar()
        self.key_bind = StringVar()
        # Set the variable value
        self._update_contents()
        self.key_bind.set("")
        # Set the label above to the variable value
        self.label["textvariable"] = self.contents
        self.label_binding["textvariable"] = self.key_bind
        custom_logger.debug(f"Created frame for pollen {self.pollen.nome}")

    def _update_contents(self) -> None:
        self.contents.set(self.pollen.short_str())

    def add(self, event) -> None:
        """Callback function to increment pollen count."""
        self.undo_stack.append(dict(self.pollen.__dict__))
        self.pollen.add()
        self._update_contents()
        self.event_generate("<<Changed>>", when="head")

    def reset(self):
        self.undo_stack = deque()
        self.redo_stack = deque()
        self.pollen.reset()
        self._update_contents()

    def set_pollen(self, pollen: Pollen):
        self.pollen = pollen
        self._update_contents()

    def undo(self):
        self.redo_stack.append(dict(self.pollen.__dict__))
        self.set_pollen(Pollen(**self.undo_stack.pop()))

    def redo(self):
        self.undo_stack.append(dict(self.pollen.__dict__))
        self.set_pollen(Pollen(**self.redo_stack.pop()))

    def set_binding(self, key: str) -> None:
        # Bind the key to increase the pollen count
        self.master.bind(f"<{key}>", self.add)
        # Set the variable
        self.key_bind.set(f"{key}")
        custom_logger.info(f"Changed binding of {self.pollen.nome} to {key}")

    @classmethod
    def generate_with_binding(
        cls: PF, master: ttk.Frame, fam: str, nome: str, key: str, count: int = 0
    ) -> PF:
        """Class method used to generate a new pollen instance
        while at the same time binding it to a keyboard key.
        """
        # Instantiate pollen object
        pln = cls(master, fam, nome, count)
        # Bind the key to increase the pollen count
        pln.set_binding(key)
        custom_logger.info(f"Generated pollen {nome} bound to key {key}")
        return pln


class EntryFrame(Toplevel, ABC):
    """This class manages the window used to save/load data."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master, takefocus=True)
        self.data = None
        self.master = master
        self.init_dir = "."
        self._grid_config()
        self.entry = ttk.Entry(self, takefocus=True, style="Generic.TEntry")
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        # Browse button
        self.button_cancel = ttk.Button(
            self, text="Browse", command=self._select_file, style="Generic.TButton"
        )
        self.button_cancel.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self._update_position()

    def _grid_config(self):
        self.geometry(f"{_TLW_WIDTH}x{_TLW_HEIGHT}")
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.resizable(0, 0)

    def _update_position(self):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        self.geometry("+%d+%d" % (x + w // 3, y + h // 3))

    @abstractmethod
    def _select_file(self):
        pass


class SaveFrame(EntryFrame):
    """Frame used to save the current count of each pollen in a CSV file."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master)
        self.function_button = ttk.Button(
            self, text="Save", command=self._save, style="Generic.TButton"
        )
        self.function_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def _select_file(self):
        dirname = filedialog.askdirectory(
            initialdir=self.init_dir, title="Select a Directory"
        )
        self.init_dir = dirname
        self.entry.delete(0, "end")
        self.entry.insert(0, dirname)

    def _save(self) -> None:
        custom_logger.info("Save data to csv file.")
        if not os.path.exists("./data"):
            os.makedirs("./data")
        filename = self.entry.get()
        filename = filename.strip().split(".")[0] + ".csv"
        if filename is not None and ".csv" in filename:
            self.data.to_csv(filename, sep=";", index=False)
            custom_logger.info(
                f"Finished saving to csv file {os.path.abspath(filename)}."
            )
            self.destroy()
        else:
            custom_logger.error("Error, wrong filename.")


class LoadFrame(EntryFrame):
    """Frame used to load the count of each pollen from a CSV file."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master)
        self.function_button = ttk.Button(
            self, text="Load", command=self._load, style="Generic.TButton"
        )
        self.function_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def _select_file(self):
        filename = filedialog.askopenfilename(
            initialdir=self.init_dir,
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*")),
        )
        self.init_dir = os.path.dirname(os.path.abspath(filename))
        self.entry.delete(0, "end")
        self.entry.insert(0, os.path.abspath(filename))

    def _load(self) -> None:
        custom_logger.info("Load data from csv file.")
        bindings = [
            "Up",
            "Down",
            "Left",
            "Right",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "x",
            "y",
            "w",
            "z",
        ]
        filename = self.entry.get()
        if filename is not None and ".csv" in filename:
            try:
                df = pd.read_csv(filename, sep=";", index_col=False)
                vals = list(df.T.to_dict().values())
                custom_logger.debug(f"Loaded pandas dataframe with data {vals}")
                # Clear previous stuff
                self.master.clear()
                self.master.add_pollens(
                    [{**vals[i], "key": bindings[i]} for i in range(len(vals))]
                )
                custom_logger.info(
                    f"Finished loading from csv file {os.path.abspath(filename)}."
                )
            except FileNotFoundError as e:
                custom_logger.error("File not found.")
                raise e
            finally:
                self.destroy()
        else:
            custom_logger.error("Error, wrong filename.")


class HelpFrame(Toplevel):
    """Frame shown when clicking the ? button."""

    def __init__(self, master: Union[ttk.Frame, Tk], help_str: str) -> None:
        super().__init__(master)
        self.master = master
        # Help text
        self.help_text = StringVar()
        self.help_text.set(help_str)
        self.text_widget = ttk.Label(self, style="Help.TLabel")
        self.text_widget.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.text_widget["textvariable"] = self.help_text
        # Cancel Button
        self.cancel_button = ttk.Button(
            self, text="Cancel", command=self.destroy, style="Generic.TButton"
        )
        self.cancel_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.resizable(1, 0)

    def set_help_text(self, text: str) -> None:
        self.help_text.set(text)


class ExtraInfoFrame(Toplevel):
    """This class manages the window used to add vetrino id and operator id."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master, takefocus=True)
        self.master = master
        self._grid_config()
        # Vetrino
        self.label_vetrino = ttk.Label(self, style="Generic.TLabel")
        self.label_vetrino.grid(row=0, column=0, padx=5, pady=5, )
        self.label_vetrino["text"] = 'Vetrino'
        self.entry_vetrino = ttk.Entry(self, takefocus=True, style="Generic.TEntry")
        text = self.master.data_extra.get('Vetrino', '')
        if isinstance(text, pd.Series):
            text = text.iloc[0]
        self.entry_vetrino.insert(0, text)
        self.entry_vetrino.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Operatore
        self.label_operator = ttk.Label(self, style="Generic.TLabel")
        self.label_operator.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        self.label_operator["text"] = 'Operatore'
        self.text_operator = Text(self, takefocus=True, background='white', padx=5, pady=5, wrap='word', height=5, width=30)
        text = self.master.data_extra.get('Operatori', '')
        if isinstance(text, pd.Series):
            text = text.iloc[0]
        self.text_operator.insert("1.0", text)
        self.text_operator.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Save button
        self.button_save = ttk.Button(
            self, text="Save", command=self._save, style="Generic.TButton"
        )
        self.button_save.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        # Cancel button
        self.button_cancel = ttk.Button(
            self, text="Cancel", command=self.destroy, style="Generic.TButton"
        )
        self.button_cancel.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self._update_position()

    def _grid_config(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.resizable(0, 1)

    def _update_position(self):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        self.geometry("+%d+%d" % (x + w // 3, y + h // 3))

    def _save(self):
        operators = self.text_operator.get("1.0", END).strip()
        vetrino = self.entry_vetrino.get().strip()
        self.master.data_extra = pd.DataFrame({'Operatori': [operators], 'Vetrino': [vetrino]})
        self.destroy()
