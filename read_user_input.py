from tkinter import Tk, ttk
from pollen_classes import generate_bindings


if __name__ == '__main__':
    root = Tk()
    generate_bindings(root)
    button = ttk.Button(root, text="Quit", command=root.destroy)
    button.grid(column=3, row=7, padx=5, pady=5)
    root.mainloop()