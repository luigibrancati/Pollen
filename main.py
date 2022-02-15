from datetime import datetime
from app import Application
import logging
import os


if __name__ == '__main__':
    app_data = os.getenv("LOCALAPPDATA")
    if app_data is not None:
        log_dir = f"{app_data}/Pollen/logs"
    else:
        log_dir = "./Pollen/logs"

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    custom_logger = logging.getLogger(name='pollen_logger')
    file_handler = logging.FileHandler(filename=f"{log_dir}/log_{datetime.now().strftime('%Y%m%dT%H%M%S')}.log")
    custom_logger.addHandler(file_handler)
    custom_logger.setLevel(logging.DEBUG)
    custom_logger.info("Starting app")

    app = Application.generate_starting_frame()  # Generate app
    app.mainloop()  # Main event loop
