from tkinter import ttk, StringVar
from __future__ import annotations


# Pollen class is used both as a pollen representation and a tkinter frame
class Pollini(ttk.Frame):
    """Class to manage different pollen types."""
 
    def __init__(self: Pollini, master: ttk.Frame, fam: str, nome: str) -> None:
        super().__init__(master) # Initialize the ttk.Frame class with a master frame
        self.master = master
        self.famiglia = fam # Family
        self.nome = nome # Name
        self.tot = 0 # Total count

        self.label = ttk.Label(self) # Tkinter label to show relevant info
        self.label.grid(column=0, row=0) # Position the label inside the Pollen frame
        # Create a string variable using tkinter class StringVar
        self.contents = StringVar()
        # Set the variable value
        self.contents.set(f"{self.famiglia}: {self.tot}")
        # Set the label above to the variable value
        self.label["textvariable"] = self.contents
    
    def add(self: Pollini, event) -> None:
        """Callback function to increment pollen count."""
        self.tot += 1

    def show(self: Pollini, event) -> None:
        """Callback function to update the label text."""
        self.contents.set(f"{self.famiglia}: {self.tot}")
        self.label["textvariable"] = self.contents

    @classmethod
    def generate_with_binding(cls: Pollini, master: ttk.Frame, fam: str, nome: str, key: str) -> Pollini:
        """Class method used to generate a new pollen instance while at the same time binding it to a keyboard key."""
        pln = cls(master, fam, nome) # Instantiate pollen object
        pln.master.bind(f"<{key}>", pln.add) # Bind the key to increase the pollen count
        pln.master.bind(f"<{key}>", pln.show, add='+') # Bind the key to also update the label value
        return pln


def generate_bindings(master: ttk.Frame) -> None:
    """Function to generate all bindings needed for the whole app."""
    padx = 10
    pady = 10
    Pollini.generate_with_binding(master, "Aceraceae", "Aceraceae", "Up").grid(column=0, row=0, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Cannabbaceae", "Cannabbaceae", "Down").grid(column=1, row=0, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Betulaceae", "Betulaceae", "Left").grid(column=2, row=0, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Alnus", "Alnus", "Right").grid(column=3, row=0, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Betula", "Betula", "a").grid(column=0, row=1, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Chenopodiaceae/Amaranthaceae", "Chenopodiaceae/Amaranthaceae", "b").grid(column=1, row=1, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Compositae", "Ambrosia", "c").grid(column=2, row=1, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Compositae", "Artemisia", "d").grid(column=3, row=1, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Corylaceae", "Carpinus", "e").grid(column=0, row=2, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Corylaceae", "Coryllus avellana", "f").grid(column=1, row=2, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Cupressaceae/Taxaceae", "Cupressaceae/Taxaceae", "g").grid(column=2, row=2, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Fagaceae", "Castanea sativa", "h").grid(column=3, row=2, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Fagaceae", "Fagus sylvatica", "i").grid(column=0, row=3, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Fagaceae", "Quercus", "j").grid(column=1, row=3, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Graminae", "Graminae", "k").grid(column=2, row=3, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Oleaceae", "Fraxinus", "l").grid(column=3, row=3, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Oleaceae", "Olea", "m").grid(column=0, row=4, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Pinaceae", "Pinaceae", "n").grid(column=1, row=4, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Plantaginaceae", "Plantaginaceae", "o").grid(column=2, row=4, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Platanaceae", "Platanaceae", "p").grid(column=3, row=4, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Polygonaceae", "Polygonaceae", "q").grid(column=0, row=5, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Salicaceae", "Populus", "r").grid(column=1, row=5, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Salicaceae", "Salix", "s").grid(column=2, row=5, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Ulmaceae", "Ulmaceae", "t").grid(column=3, row=5, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Uritcaceae", "Uritcaceae", "u").grid(column=0, row=6, padx=padx, pady=pady)
    Pollini.generate_with_binding(master, "Alternaria", "Alternaria", "w").grid(column=1, row=6, padx=padx, pady=pady)