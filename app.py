from __future__ import annotations
from tkinter import ttk, StringVar
import pandas as pd
import json


# Pollen class is used both as a pollen representation and a tkinter frame
class Pollini(ttk.Frame):
    """Class to manage different pollen types."""

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

    def update_count(self, event) -> None:
        """Callback function to update the label text."""
        self.contents.set(f"{self.famiglia}: {self.tot}")
        self.label["textvariable"] = self.contents

    @property
    def __dict__(self) -> dict:
        return {"famiglia": self.famiglia,
                "nome": self.nome,
                "conteggio": self.tot}

    @classmethod
    def generate_with_binding(cls: Pollini, master: ttk.Frame, fam: str,
                              nome: str, key: str, count: int = 0) -> Pollini:
        """Class method used to generate a new pollen instance
        while at the same time binding it to a keyboard key.
        """
        # Instantiate pollen object
        pln = cls(master, fam, nome, count)
        # Bind the key to increase the pollen count
        pln.master.bind(f"<{key}>", pln.add)
        # Bind the key to also update the label value
        pln.master.bind(f"<{key}>", pln.update_count, add='+')
        pln.key_bind.set(f"{key}")
        return pln


class Application():
    """Class to manage the pollen grid and placement,
    along with external buttons.
    """
    def __init__(self: Application, master: ttk.Frame, cols: int) -> None:
        self.master = master
        self.cols = cols
        self.pollen_frames = []

        # Load button
        self.button_load = ttk.Button(self.master, text="Load",
                                      command=self.load)
        # Save button
        self.button_save = ttk.Button(self.master, text="Save",
                                      command=self.save)
        # Quit button
        self.button_quit = ttk.Button(self.master, text="Quit",
                                      command=self.master.destroy)
        self.id_entry = ttk.Entry(self.master)
        self.id_entry.bind("<Return>", self.focus_on_master)

    def focus_on_master(self, event):
        return self.master.focus()

    def add_pollens(self, pollens: list[dict[str, str, str]]) -> None:
        """Function to generate all bindings needed for the whole app."""
        for pollen in pollens:
            try:
                pln = Pollini.generate_with_binding(self.master,
                                                    pollen['famiglia'],
                                                    pollen['nome'],
                                                    pollen['key'],
                                                    pollen['conteggio'])
            except KeyError:
                pln = Pollini.generate_with_binding(self.master,
                                                    pollen['famiglia'],
                                                    pollen['nome'],
                                                    pollen['key'])
            self.pollen_frames.append(pln)

    def add_standard_pollens(self):
        with open('./standard_pollen_mapping.json') as file:
            self.add_pollens(json.load(file))

    def draw_grid(self):
        # Place pollens in frame
        self.id_entry.grid(column=0, row=0, padx=5, pady=5)

        for i, pollen in enumerate(self.pollen_frames):
            col = i % self.cols
            row = i // self.cols + 1
            pollen.grid(column=col, row=row, padx=10, pady=10)

        n_plns = len(self.pollen_frames)
        self.button_load.grid(column=self.cols-3, row=n_plns+1, padx=5, pady=5)
        self.button_save.grid(column=self.cols-2, row=n_plns+1, padx=5, pady=5)
        self.button_quit.grid(column=self.cols-1, row=n_plns+1, padx=5, pady=5)

    def save(self) -> None:
        id = self.id_entry.get()
        if id:
            df = pd.DataFrame([vars(pln) for pln in self.pollen_frames])
            df.to_csv(f'./Vetrino_{id}.csv', sep=';', index=False)
        else:
            print("Error, id not set.")

    def load(self) -> None:
        bindings = ["Up", "Down", "Left", "Right", "a", "b",
                    "c", "d", "e", "f", "g", "h", "i", "j",
                    "k", "l", "m", "n", "o", "p", "q", "r",
                    "s", "t", "u", "w"]
        if id:
            filename = f'./Vetrino_{self.id_entry.get()}.csv'
            df = pd.read_csv(filename, sep=';', index_col=False)
            self.pollen_frames = []
            vals = list(df.T.to_dict().values())
            self.add_pollens(
                [{**vals[i], 'key': bindings[i]} for i in range(len(vals))]
            )
            self.draw_grid()
        else:
            print("Error, id not set.")

    @classmethod
    def generate_starting_frame(cls, master: ttk.Frame, cols: int = 5):
        app = Application(master, cols)
        app.add_standard_pollens()
        app.draw_grid()
        return app
