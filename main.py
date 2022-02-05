from datetime import datetime
from app import Application
import logging
import os


if not os.path.exists("./.logs"):
    os.makedirs("./.logs")
logging.basicConfig(filename=f'./.logs/{datetime.now()}.log',
                    level=logging.INFO)


if __name__ == '__main__':
    logging.debug("Starting app")
    app = Application.generate_starting_frame()  # Generate app
    app.mainloop()  # Main event loop
