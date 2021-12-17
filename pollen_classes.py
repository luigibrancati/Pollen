from tkinter import ttk, StringVar


class Pollini(ttk.Frame):
    def __init__(self, master, fam, nome):
        super().__init__(master)
        self.master = master

        self.famiglia = fam
        self.nome = nome
        self.tot = 0

        self.label = ttk.Label(self)
        self.label.grid(column=0, row=0)
        # Create the application variable.
        self.contents = StringVar()
        # Set it to some value.
        self.contents.set(f"{self.famiglia}: {self.tot}")
        # Tell the entry widget to watch this variable.
        self.label["textvariable"] = self.contents
    
    def add(self, event):
        self.tot += 1

    def show(self, event):
        self.contents.set(f"{self.famiglia}: {self.tot}")
        self.label["textvariable"] = self.contents

    @classmethod
    def generate_with_binding(cls, master, fam, nome, key):
        pln = cls(master, fam, nome)
        pln.master.bind(f"<{key}>", pln.add)
        pln.master.bind(f"<{key}>", pln.show, add='+')
        return pln


def generate_bindings(master):
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