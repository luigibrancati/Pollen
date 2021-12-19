from tkinter import Tk
from pollen_classes import generate_frame


if __name__ == '__main__':
    root = Tk() # main Frame object
    generate_frame(root) # Generate bindings
    root.mainloop() # main event loop