from collections import deque
from datetime import datetime
from multiprocessing.sharedctypes import Value
from config import _TLW_HEIGHT, _TLW_WIDTH
from pollen_class import Pollen
from tkinter import END, Toplevel, ttk, StringVar, Tk, filedialog, Text
from typing import TypeVar, Union
import pandas as pd
import os
import logging
from abc import ABC, abstractmethod
import json


custom_logger = logging.getLogger(name="pollen_logger")
PF = TypeVar("PF", bound="PollenFrame")


# Pollen class is used both as a pollen representation and a tkinter frame
class PollenFrame(ttk.Frame):
    """Class to manage different pollen types.
    This class contains data about the pollen family, name and count.
    It also manages the frame to represent the pollen family
    and its key binding.
    """

    def __init__(self, master: ttk.Frame, fam: str, nome: str, use_family: bool, count: int = 0) -> None:
        # Initialize the ttk.Frame class with a master frame
        super().__init__(master)
        self.master = master
        self.pollen = Pollen(fam, nome, use_family, count)
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

    def set_binding(self, key: Union[str, int]) -> None:
        # Bind the key to increase the pollen count
        key = str(key)
        if PollenFrame.is_number_key(key):
            self.master.bind(key, self.add)
        else:
            self.master.bind(f"<{key}>", self.add)
        # Set the variable
        self.key_bind.set(f"{key}")
        custom_logger.info(f"Changed binding of {self.pollen.nome} to {key}")

    @staticmethod
    def is_number_key(key: str):
        try:
            return int(key) in range(10)
        except ValueError:
            return False

    @classmethod
    def generate_with_binding(
        cls: PF, master: ttk.Frame, fam: str, nome: str, key: str, use_family: bool, count: int = 0
    ) -> PF:
        """Class method used to generate a new pollen instance
        while at the same time binding it to a keyboard key.
        """
        # Instantiate pollen object
        pln = cls(master, fam, nome, use_family, count)
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
        self.entry = ttk.Entry(self, takefocus=True, style="Generic.TEntry", width=100)
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        # Browse button
        self.button_cancel = ttk.Button(
            self, text="Cerca", command=self._select_file, style="Generic.TButton"
        )
        self.button_cancel.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self._update_position()

    def _grid_config(self):
        self.geometry(f"{_TLW_WIDTH}x{_TLW_HEIGHT}")
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.resizable(1, 0)

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
            self, text="Salva", command=self._save, style="Generic.TButton"
        )
        self.function_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        self.data = SaveFrame._data_fields_to_save(pd.DataFrame([vars(plnf.pollen) for plnf in self.master.pollen_frames]))
        self.metadata = self.master.data_extra

    @staticmethod
    def _data_fields_to_save(df):
        return df[['nome', 'famiglia', 'conteggio']]

    def _select_file(self):
        dirname = filedialog.askdirectory(
            initialdir=self.init_dir,
            title="Seleziona una cartella"
        )
        self.init_dir = dirname
        self.entry.delete(0, "end")
        self.entry.insert(0, dirname)

    def _save(self) -> None:
        custom_logger.info("Save data to csv file.")
        if not os.path.exists("./data"):
            os.makedirs("./data")
        filename = self.entry.get()
        filename = filename.strip().split(".")[0]
        if filename is not None:
            self.metadata.to_csv(f"{filename}.csv", sep=";", index=False, mode='w')
            self.data.to_csv(f"{filename}.csv", sep=";", index=False, mode='a')
            custom_logger.info(
                f"Finished saving data to csv file {os.path.abspath(filename)}."
            )
            self.destroy()
        else:
            custom_logger.error("Error, wrong filename.")


class LoadFrame(EntryFrame):
    """Frame used to load the count of each pollen from a CSV file."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master)
        self.function_button = ttk.Button(
            self, text="Carica", command=self._load, style="Generic.TButton"
        )
        self.function_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    @staticmethod
    def _load_config():
        with open('./configuration.json', 'r') as f:
            custom_logger.info("Read configuration file.")
            return json.load(f)

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
        filename = self.entry.get().strip()
        if filename is not None and ".csv" in filename:
            try:
                configuration = pd.DataFrame(LoadFrame._load_config()['pollens'])
                df_data = pd.read_csv(filename, sep=";", index_col=False, header=2).merge(configuration, how='left', on=['famiglia', 'nome'])
                # Remove pollens without a binding in configuration
                df_data.dropna(subset=['key'], inplace=True, axis=0)
                # Create pollen frames
                vals = list(df_data.T.to_dict().values())
                custom_logger.debug(f"Loaded pandas dataframe with data {vals}")
                self.master.clear()
                self.master.add_pollens(vals)
                custom_logger.info(
                    f"Finished loading from csv file {os.path.abspath(filename)}."
                )
                # Add metadata
                self.master.data_extra = pd.read_csv(filename, sep=";", index_col=False, nrows=1)
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
            self, text="Chiudi", command=self.destroy, style="Generic.TButton"
        )
        self.cancel_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.resizable(0, 0)

    def set_help_text(self, text: str) -> None:
        self.help_text.set(text)


class ExtraInfoFrame(Toplevel):
    """This class manages the window used to add vetrino id and operator id."""

    def __init__(self, master: Union[ttk.Frame, Tk]) -> None:
        super().__init__(master, takefocus=True)
        self.master = master
        self._grid_config()
        # Operatore
        ttk.Label(self, text='Operatore', style="Generic.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="en")
        self.entry_operatore = ttk.Entry(self, takefocus=True, style="Generic.TEntry")
        text = self.master.data_extra.get('operatore', '')
        if isinstance(text, pd.Series):
            text = text.iloc[0]
        self.entry_operatore.insert(0, text)
        self.entry_operatore.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Data
        ttk.Label(self, text='Data (gg/mm/aaaa)', style="Generic.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="en")
        self.entry_data = ttk.Entry(self, takefocus=True, style="Generic.TEntry")
        text = self.master.data_extra.get('data', ExtraInfoFrame._now_date())
        if isinstance(text, pd.Series):
            text = text.iloc[0]
        self.entry_data.insert(0, text)
        self.entry_data.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.entry_data.config(
            validate="focusout",
            validatecommand=(self.register(self._validate_date), '%P'),
            invalidcommand=self._on_invalid
        )
        # Validation
        self.label_error = ttk.Label(self, text='', style="Error.TLabel")
        self.label_error.grid(row=2, column=1, padx=5, pady=5, sticky="wn")
        # Vetrino
        ttk.Label(self, text='Linee vetrino', style="Generic.TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="en")
        self.text_vetrino = Text(self, takefocus=True, background='white', padx=5, pady=5, wrap='word', height=5, width=55)
        text = self.master.data_extra.get('linee_vetrino', '')
        if isinstance(text, pd.Series):
            text = text.iloc[0]
        self.text_vetrino.insert("1.0", text)
        self.text_vetrino.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Save button
        self.button_save = ttk.Button(
            self, text="Salva", command=self._save, style="Generic.TButton"
        )
        self.button_save.grid(row=4, column=1, padx=5, pady=5, sticky="e")
        # Cancel button
        self.button_cancel = ttk.Button(
            self, text="Annulla", command=self.destroy, style="Generic.TButton"
        )
        self.button_cancel.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        self._update_position()

    def _grid_config(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.resizable(1, 1)

    def _update_position(self):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        self.geometry("+%d+%d" % (x + w // 3, y + h // 3))

    def _save(self):
        operator = self.entry_operatore.get().strip()
        data = self.entry_data.get().strip()
        vetrino = self.text_vetrino.get("1.0", END).strip()
        self.master.data_extra = pd.DataFrame({'operatore': [operator], 'data': [data], 'linee_vetrino': [vetrino]})
        self.destroy()

    @staticmethod
    def _now_date():
        return datetime.now().date().strftime('%d/%m/%Y')

    def _validate_date(self, date):
        try:
            datetime.strptime(date, '%d/%m/%Y')
            self.label_error['text'] = ''
            return True
        except ValueError:
            return False

    def _on_invalid(self):
        self.label_error['text'] = 'La data non è nel formato atteso gg/mm/aaaa'
