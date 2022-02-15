from config import _TLW_HEIGHT, _TLW_WIDTH
from pollen_class import Pollen
from tkinter import Toplevel, ttk, StringVar, Tk, filedialog
from typing import TypeVar, Union
import pandas as pd
import os
import logging
from abc import ABC, abstractmethod


PF = TypeVar("PF", bound="PollenFrame")


# Pollen class is used both as a pollen representation and a tkinter frame
class PollenFrame(ttk.Frame):
    """Class to manage different pollen types.
    This class contains data about the pollen family, name and count.
    It also manages the frame to represent the pollen family
    and its key binding.
    """

    def __init__(self, master: ttk.Frame, fam: str, nome: str,
                 count: int = 0) -> None:
        # Initialize the ttk.Frame class with a master frame
        super().__init__(master)
        self.master = master
        self.pollen = Pollen(fam, nome, count)
        # Tkinter labels to show relevant info
        self.label = ttk.Label(self)
        self.label.grid(column=1, row=0, padx=5)
        self.label_binding = ttk.Label(self,
                                       borderwidth=3,
                                       relief="raised",
                                       padding=5)
        self.label_binding.grid(column=0, row=0, padx=5)
        # Create a string variable using tkinter class StringVar
        self.contents = StringVar()
        self.key_bind = StringVar()
        # Set the variable value
        self.update_contents()
        self.key_bind.set("")
        # Set the label above to the variable value
        self.label["textvariable"] = self.contents
        self.label_binding["textvariable"] = self.key_bind
        logging.debug(f"Created frame for pollen {self.pollen.nome}")

    def update_contents(self) -> None:
        self.contents.set(self.pollen.short_str())

    def add(self, event) -> None:
        """Callback function to increment pollen count."""
        self.master._add_to_undo(dict(self.pollen.__dict__))
        self.pollen.add()
        self.update_contents()

    def reset(self):
        self.pollen.reset()
        self.update_contents()

    def set_pollen(self, pollen: Pollen):
        self.pollen = pollen
        self.update_contents()

    def set_binding(self, key: str) -> None:
        # Bind the key to increase the pollen count
        self.master.bind(f"<{key}>", self.add)
        # Set the variable
        self.key_bind.set(f"{key}")
        logging.info(f"Changed binding of {self.pollen.nome} to {key}")

    @classmethod
    def generate_with_binding(cls: PF,
                              master: ttk.Frame,
                              fam: str,
                              nome: str,
                              key: str,
                              count: int = 0) -> PF:
        """Class method used to generate a new pollen instance
        while at the same time binding it to a keyboard key.
        """
        # Instantiate pollen object
        pln = cls(master, fam, nome, count)
        # Bind the key to increase the pollen count
        pln.set_binding(key)
        logging.info(f"Generated pollen {nome} bound to key {key}")
        return pln


class EntryFrame(Toplevel, ABC):
    """This class manages the window used to save/load data."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master, takefocus=True)
        self.data = None
        self.master = master
        self.init_dir = "."
        self._grid_config()
        self.entry = ttk.Entry(self, takefocus=True)
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        # Browse button
        self.button_cancel = ttk.Button(self, text="Browse", command=self._select_file)
        self.button_cancel.grid(row=0, column=2, padx=5, pady=5, sticky="E")
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
        self.geometry("+%d+%d" % (x + w//3, y + h//3))

    @abstractmethod
    def _select_file(self):
        pass


class SaveFrame(EntryFrame):
    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master)
        self.function_button = ttk.Button(self, text="Save", command=self._save)
        self.function_button.grid(row=0, column=1, padx=5, pady=5, sticky="E")

    def _select_file(self):
        dirname = filedialog.askdirectory(
            initialdir=self.init_dir,
            title="Select a Directory"
        )
        self.init_dir = dirname
        self.entry.delete(0, "end")
        self.entry.insert(0, dirname)

    def _save(self) -> None:
        logging.info("Save data to csv file.")
        if not os.path.exists("./data"):
            os.makedirs("./data")
        filename = self.entry.get()
        if filename is not None and '.csv' in filename:
            self.data.to_csv(filename, sep=';', index=False)
            logging.info(f"Finished saving to csv file {os.path.abspath(filename)}.")
            self.destroy()
        else:
            logging.error("Error, wrong filename.")


class LoadFrame(EntryFrame):
    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master)
        self.function_button = ttk.Button(self, text="Load", command=self._load)
        self.function_button.grid(row=0, column=1, padx=5, pady=5, sticky="E")

    def _select_file(self):
        filename = filedialog.askopenfilename(
            initialdir=self.init_dir,
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
        )
        self.init_dir = os.path.dirname(os.path.abspath(filename))
        self.entry.delete(0, "end")
        self.entry.insert(0, os.path.abspath(filename))

    def _load(self) -> None:
        logging.info("Load data from csv file.")
        bindings = ["Up", "Down", "Left", "Right", "a", "b",
                    "c", "d", "e", "f", "g", "h", "i", "j",
                    "k", "l", "m", "n", "o", "p", "q", "r",
                    "s", "t", "u", "v", "x", "y", "w", "z"]
        filename = self.entry.get()
        if filename is not None and '.csv' in filename:
            try:
                df = pd.read_csv(filename, sep=';', index_col=False)
                vals = list(df.T.to_dict().values())
                logging.debug(f"Loaded pandas dataframe with data {vals}")
                self.master.clear()  # Clear previous stuff
                self.master.add_pollens(
                    [{**vals[i], 'key': bindings[i]} for i in range(len(vals))]
                )
                logging.info(f"Finished loading from csv file {os.path.abspath(filename)}.")
            except FileNotFoundError as e:
                logging.error("File not found.")
                raise e
            finally:
                self.destroy()
        else:
            logging.error("Error, wrong filename.")
