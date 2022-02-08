import pandas as pd
import logging
from typing import TypeVar, Dict, List
from frames import SaveFrame, LoadFrame, PollenFrame
from tkinter import ttk, Tk
from pollen_class import STANDARD_POLLEN


A = TypeVar("A", bound="Application")


class Application(Tk):
    """Class to manage the pollen grid and placement,
    along with external buttons.
    """

    def __init__(self, cols: int) -> None:
        super().__init__()
        self.title("Pollen Register")
        self.cols = cols
        self.pollen_frames = []

        # Reset count button
        self.button_reset_count = ttk.Button(self, text="Reset count",
                                             command=self._reset_count)
        # Load button
        self.button_load = ttk.Button(self, text="Load",
                                      command=self._load)
        # Save button
        self.button_save = ttk.Button(self, text="Save",
                                      command=self._save)
        # Quit button
        self.button_quit = ttk.Button(self, text="Quit",
                                      command=self.destroy)

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
        logging.info("Reset pollen count.")
        for p in self.pollen_frames:
            p.reset()

    def _load(self) -> None:
        id_frame = LoadFrame(self)
        id_frame.title("Load")
        id_frame.mainloop()

    def _save(self) -> None:
        id_frame = SaveFrame(self)
        id_frame.title("Save")
        id_frame.data = pd.DataFrame([vars(plnf.pollen) for plnf in self.pollen_frames])
        id_frame.mainloop()

    def clear(self):
        self.pollen_frames = []

    def add_pollens(self, pollens: List[Dict[str, str]]) -> None:
        """Function to generate all bindings needed for the whole app."""
        logging.info("Add pollens.")
        for pollen in pollens:
            try:
                pln = PollenFrame.generate_with_binding(self,
                                                        pollen['famiglia'],
                                                        pollen['nome'],
                                                        pollen['key'],
                                                        pollen['conteggio'])
            except KeyError:
                logging.warning("Field 'conteggio' not found as a key!")
                pln = PollenFrame.generate_with_binding(self,
                                                        pollen['famiglia'],
                                                        pollen['nome'],
                                                        pollen['key'])
            logging.info(f"Added pollen {pln.pollen.nome}")
            self.pollen_frames.append(pln)
        # We redraw the grid
        # This is need when we need to add new pollens later
        logging.info("Finished adding pollens.")
        self._draw_grid()

    def add_standard_pollens(self):
        logging.info("Adding all standard pollens.")
        self.add_pollens(STANDARD_POLLEN)
        logging.info("Finished adding standard pollens.")
        self._draw_grid()

    @classmethod
    def generate_starting_frame(cls, cols: int = 5) -> A:
        app = Application(cols)
        app.add_standard_pollens()
        logging.info("Application generated.")
        return app
