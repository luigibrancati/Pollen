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
    logging.basicConfig(filename=f"{log_dir}/log_{datetime.now().strftime('%Y%m%dT%H%M%S')}.log",
                        level=logging.WARNING)

    logging.debug("Starting app")
    app = Application.generate_starting_frame()  # Generate app
    app.mainloop()  # Main event loop
