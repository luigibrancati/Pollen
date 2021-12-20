from tkinter import Tk
from app import Application


if __name__ == '__main__':
    root = Tk()  # Main Frame object
    Application.generate_starting_frame(root)  # Generate bindings
    root.mainloop()  # Main event loop
