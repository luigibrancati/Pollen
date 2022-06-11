from datetime import datetime
from app import Application
from tkinter import ttk
from config import _FONT
import logging
import os
import platform


if __name__ == "__main__":
    # Create logs directory based on OS
    if "windows" in platform.system().lower():
        app_data_dir = os.getenv("LOCALAPPDATA") or "."
        pollen_dir = os.path.join(app_data_dir, "Pollen")
    else:
        app_data_dir = os.getenv("HOME") or "."
        pollen_dir = os.path.join(app_data_dir, ".pollen")
    log_dir = os.path.join(pollen_dir, "logs")
    if not os.path.exists(pollen_dir):
        os.makedirs(pollen_dir)
        os.makedirs(log_dir)
    else:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    custom_logger = logging.getLogger(name="pollen_logger")
    file_handler = logging.FileHandler(
        filename=f"{log_dir}/log_{datetime.now().strftime('%Y%m%dT%H%M%S')}.log"
    )
    custom_logger.addHandler(file_handler)
    custom_logger.setLevel(logging.DEBUG)
    custom_logger.info("Starting app")

    # Generate app
    app = Application.start()

    # Custom styles
    style = ttk.Style(app)
    style.configure("Generic.TLabel", padding=5, font=(_FONT, 10))
    style.configure("Generic.TButton", padding=5, font=(_FONT, 10))
    style.configure(
        "Generic.TEntry",
        foreground="black",
        background="white",
        padding=5,
        font=(_FONT, 10)
    )
    style.configure(
        "BindKey.TLabel", padding=5, borderwidth=3, relief="groove", font=(_FONT, 10)
    )
    style.configure("Help.TButton", padding=5, font=(_FONT, 10), width=2)
    style.configure(
        "Help.TLabel",
        justify="left",
        relief="groove",
        foreground="black",
        background="white",
        padding=10,
        font=(_FONT, 11),
    )

    # Main event loop
    app.mainloop()
