from __future__ import annotations
from tkinter import Toplevel, ttk, StringVar, Tk
import pandas as pd
import json


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
        self.famiglia = fam  # Family
        self.nome = nome  # Name
        self.tot = count  # Total count

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
        self.contents.set(f"{self.famiglia}: {self.tot}")
        self.key_bind.set("")
        # Set the label above to the variable value
        self.label["textvariable"] = self.contents
        self.label_binding["textvariable"] = self.key_bind

    def add(self, event) -> None:
        """Callback function to increment pollen count."""
        self.tot += 1
        self.contents.set(f"{self.famiglia}: {self.tot}")

    def reset_count(self):
        self.tot = 0
        self.contents.set(f"{self.famiglia}: {self.tot}")

    def set_binding(self, key: str) -> None:
        # Bind the key to increase the pollen count
        self.master.bind(f"<{key}>", self.add)
        # Set the variable
        self.key_bind.set(f"{key}")

    @property
    def __dict__(self) -> dict:
        return {"famiglia": self.famiglia,
                "nome": self.nome,
                "conteggio": self.tot}

    @classmethod
    def generate_with_binding(cls: PollenFrame,
                              master: ttk.Frame,
                              fam: str,
                              nome: str,
                              key: str,
                              count: int = 0) -> PollenFrame:
        """Class method used to generate a new pollen instance
        while at the same time binding it to a keyboard key.
        """
        # Instantiate pollen object
        pln = cls(master, fam, nome, count)
        # Bind the key to increase the pollen count
        pln.set_binding(key)
        return pln


class EntryFrame(Toplevel):
    """This class opens a new window used to save/load data."""

    def __init__(self, master: ttk.Frame | Tk, save: bool = True,
                 *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.data = None
        self.master = master
        self.entry = ttk.Entry(self, takefocus=True)
        self.entry.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        # Cancel button
        self.button_cancel = ttk.Button(self, text="Cancel",
                                        command=self.destroy)
        self.button_cancel.grid(row=1, column=2, padx=5, pady=5)

        if save:
            # Save button
            self.function_button = ttk.Button(self, text="Save",
                                              command=self._save)
        else:
            # Load button
            self.function_button = ttk.Button(self, text="Load",
                                              command=self._load)
        self.function_button.grid(row=1, column=1, padx=5, pady=5)

    def _save(self) -> None:
        id = self.entry.get()
        if id:
            self.data.to_csv(f'./Vetrino_{id}.csv', sep=';', index=False)
            self.destroy()
        else:
            print("Error, id not set.")

    def _load(self) -> None:
        bindings = ["Up", "Down", "Left", "Right", "a", "b",
                    "c", "d", "e", "f", "g", "h", "i", "j",
                    "k", "l", "m", "n", "o", "p", "q", "r",
                    "s", "t", "u", "v"]
        id = self.entry.get()
        if id:
            filename = f'./Vetrino_{id}.csv'
            df = pd.read_csv(filename, sep=';', index_col=False)
            vals = list(df.T.to_dict().values())
            self.master.clear()
            self.master.add_pollens(
                [{**vals[i], 'key': bindings[i]} for i in range(len(vals))]
            )
            self.destroy()
        else:
            print("Error, id not set.")


class Application(Tk):
    """Class to manage the pollen grid and placement,
    along with external buttons.
    """

    def __init__(self, cols: int) -> None:
        super().__init__()
        self.title("Pollen Register")
        self.cols = cols
        self.pollen_frames = []

        # Load button
        self.button_load = ttk.Button(self, text="Load",
                                      command=self._load)
        # Save button
        self.button_save = ttk.Button(self, text="Save",
                                      command=self._save)
        # Quit button
        self.button_quit = ttk.Button(self, text="Quit",
                                      command=self.destroy)
        # Reset count button
        self.button_reset_count = ttk.Button(self, text="Reset count",
                                             command=self._reset_count)

    def _draw_grid(self):
        # Place pollens in frame master
        for i, pollen in enumerate(self.pollen_frames):
            # Calculate the position of each pollen family
            col = i % self.cols
            row = i // self.cols + 1
            pollen.grid(column=col, row=row, padx=10, pady=10)

        n_plns = len(self.pollen_frames)
        self.button_reset_count.grid(column=self.cols-4, row=n_plns+1,
                                     padx=5, pady=5)
        self.button_load.grid(column=self.cols-3, row=n_plns+1, padx=5, pady=5)
        self.button_save.grid(column=self.cols-2, row=n_plns+1, padx=5, pady=5)
        self.button_quit.grid(column=self.cols-1, row=n_plns+1, padx=5, pady=5)

    def _reset_count(self):
        for p in self.pollen_frames:
            p.reset_count()

    def clear(self):
        self.pollen_frames = []

    def add_pollens(self, pollens: list[dict[str, str, str]]) -> None:
        """Function to generate all bindings needed for the whole app."""
        for pollen in pollens:
            try:
                pln = PollenFrame.generate_with_binding(self,
                                                        pollen['famiglia'],
                                                        pollen['nome'],
                                                        pollen['key'],
                                                        pollen['conteggio'])
            except KeyError:
                pln = PollenFrame.generate_with_binding(self,
                                                        pollen['famiglia'],
                                                        pollen['nome'],
                                                        pollen['key'])
            self.pollen_frames.append(pln)
        self._draw_grid()

    def add_standard_pollens(self):
        with open('./standard_pollen_mapping.json') as file:
            self.add_pollens(json.load(file))
        self._draw_grid()

    def _save(self) -> None:
        id_frame = EntryFrame(self)
        id_frame.title("Save")
        id_frame.data = pd.DataFrame([vars(pln) for pln in self.pollen_frames])
        id_frame.mainloop()

    def _load(self) -> None:
        id_frame = EntryFrame(self, save=False)
        id_frame.title("Load")
        id_frame.mainloop()

    @classmethod
    def generate_starting_frame(cls, cols: int = 5) -> Application:
        app = Application(cols)
        app.add_standard_pollens()
        return app
