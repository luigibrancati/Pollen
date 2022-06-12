import pandas as pd
import logging
from typing import TypeVar, Dict, List
from frames import SaveFrame, LoadFrame, PollenFrame, HelpFrame, ExtraInfoFrame
from tkinter import ttk, Tk
from config import _UNDO_KEY, _REDO_KEY, _UNDO_KEY_HELP, _REDO_KEY_HELP, _GOOGLE_FORM_URL, _HELP_TEXT, _GOOGLE_FORM_TEXT
from collections import deque
import webbrowser

custom_logger = logging.getLogger(name="pollen_logger")
A = TypeVar("A", bound="Application")


class Application(Tk):
    """Class to manage the pollen grid and placement,
    along with external buttons.
    """

    def __init__(self, rows: int = 2, cols: int = 1) -> None:
        super().__init__()
        self.title("Pollen Register")
        self.cols = cols
        self.rows = rows
        # A list to keep all pollen frames
        self.pollen_frames = []
        self.data_extra = pd.DataFrame([])
        # Stacks to implement the undo and redo functionality
        # These stacks don't actually keep the states of the pollen counts
        # but only references to the widget that changed
        # This way, the PollenFrame manage the undo/redo individually
        # whereas the app orchestrate their turns
        self.undo_stack = deque()
        self.redo_stack = deque()
        # Add buttons inside a separate Frame
        self.button_frame = ttk.Frame(self)
        # Add footer inside a separate Frame
        self.footer_frame = ttk.Frame(self)
        # Undo and Redo bindings
        self.bind(f"<{_UNDO_KEY}>", self.undo)
        self.bind(f"<{_REDO_KEY}>", self.redo)
        self.bind("<<Changed>>", lambda event: self.undo_stack.append(event.widget))

    def _grid_config(self):
        for i in range(self.cols):
            self.columnconfigure(i, weight=1)
        for i in range(self.rows):
            self.rowconfigure(i, weight=1)
        self.resizable(0, 0)

    def _draw_grid(self):
        # Place pollens in frame master
        for i, pollen in enumerate(self.pollen_frames):
            # Calculate the position of each pollen family
            col = i % self.cols
            row = i // self.cols + 1
            pollen.grid(column=col, row=row, padx=10, pady=10, sticky="w")
        # Recompute rows in case they changed (not enough specified in configuration)
        self.rows = row + 2
        # Add buttons inside a separate Frame
        # Destroy it before to avoid duplicates due to pack
        self.button_frame.destroy()
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(
            column=0, row=self.rows - 1, columnspan=self.cols, padx=10, pady=10, sticky="e"
        )
        # Buttons: Reset count, Load, Save, Quit, Help
        self.buttons = [
            ttk.Button(
                self.button_frame,
                text="Extra Info",
                command=self._extra_info,
                style="Generic.TButton",
            ),
            ttk.Button(
                self.button_frame,
                text="Reset conteggio",
                command=self._reset_count,
                style="Generic.TButton",
            ),
            ttk.Button(
                self.button_frame,
                text="Carica file",
                command=self._load,
                style="Generic.TButton",
            ),
            ttk.Button(
                self.button_frame,
                text="Salva file",
                command=self._save,
                style="Generic.TButton",
            ),
            ttk.Button(
                self.button_frame,
                text="Chiudi",
                command=self.destroy,
                style="Generic.TButton",
            ),
            ttk.Button(
                self.button_frame, text="?", command=self._help, style="Help.TButton"
            ),
        ]
        for i, button in enumerate(self.buttons):
            # button.grid(column=i, row=0, padx=5, sticky="e")
            button.pack(padx=5, side='left')
        # Add footer inside a separate Frame
        # Destroy it before to avoid duplicates due to pack
        self.footer_frame.destroy()
        self.footer_frame = ttk.Frame(self)
        self.footer_frame.grid(
            column=0, row=self.rows, columnspan=self.cols, pady=5, padx=10
        )
        google_form_label = ttk.Label(self.footer_frame, text=_GOOGLE_FORM_TEXT, style='Footer.TLabel', justify='center')
        google_form_label.pack()
        google_form_label.bind("<Button-1>", lambda e: webbrowser.open_new(_GOOGLE_FORM_URL))
        # Grid config
        self._grid_config()

    def _extra_info(self) -> None:
        id_frame = ExtraInfoFrame(self)
        id_frame.title("Exrta info")
        id_frame.mainloop()

    def _reset_count(self):
        custom_logger.info("Reset pollen count and stacks.")
        self.undo_stack = deque()
        self.redo_stack = deque()
        for p in self.pollen_frames:
            p.reset()

    def _help(self) -> None:
        help_frame = HelpFrame(
            self,
            _HELP_TEXT.format(_UNDO_KEY_HELP, _REDO_KEY_HELP)
        )
        help_frame.title("Aiuto")
        help_frame.mainloop()

    def _load(self) -> None:
        id_frame = LoadFrame(self)
        id_frame.title("Carica file")
        id_frame.mainloop()

    def _save(self) -> None:
        id_frame = SaveFrame(self)
        id_frame.title("Salva file")
        id_frame.mainloop()

    def undo(self, event) -> None:
        try:
            widget = self.undo_stack.pop()
            self.redo_stack.append(widget)
            widget.undo()
        except IndexError as e:
            custom_logger.info(f"{e}")

    def redo(self, event) -> None:
        try:
            widget = self.redo_stack.pop()
            self.undo_stack.append(widget)
            widget.redo()
        except IndexError as e:
            custom_logger.info(f"{e}")

    def clear(self):
        self.pollen_frames = []
        self.undo_stack = deque()
        self.redo_stack = deque()

    def add_pollens(self, pollens: List[Dict[str, str]]) -> None:
        """Function to generate all bindings needed for the whole app."""
        custom_logger.info("Add pollens.")
        for pollen in pollens:
            try:
                pln = PollenFrame.generate_with_binding(
                    self,
                    pollen["famiglia"],
                    pollen["nome"],
                    pollen["key"],
                    pollen["use_family"],
                    pollen["conteggio"],
                )
            except KeyError:
                pln = PollenFrame.generate_with_binding(
                    self,
                    pollen["famiglia"],
                    pollen["nome"],
                    pollen["key"],
                    pollen["use_family"]
                )
            custom_logger.info(f"Added pollen {pln.pollen.famiglia} - {pln.pollen.nome}")
            self.pollen_frames.append(pln)
        # We redraw the grid
        custom_logger.info("Finished adding pollens.")
        self._draw_grid()

    @classmethod
    def start(cls) -> A:
        config = LoadFrame._load_config()['general']
        app = Application(config['rows'], config['columns'])
        custom_logger.info("Adding all standard pollens.")
        app.add_pollens(LoadFrame._load_config()['pollens'])
        custom_logger.info("Finished adding standard pollens.")
        custom_logger.info("Application generated.")
        return app
