from __future__ import annotations
from tkinter import ttk, StringVar
import pandas as pd
from datetime import datetime

# Pollen class is used both as a pollen representation and a tkinter frame
class Pollini(ttk.Frame):
    """Class to manage different pollen types."""
 
    def __init__(self, master: ttk.Frame, fam: str, nome: str, count: int=0) -> None:
        super().__init__(master) # Initialize the ttk.Frame class with a master frame
        self.master = master
        self.famiglia = fam # Family
        self.nome = nome # Name
        self.tot = count # Total count

        self.label = ttk.Label(self) # Tkinter label to show relevant info
        self.label.grid(column=1, row=0, padx=5) # Position the label inside the Pollen frame
        self.label_binding = ttk.Label(self, borderwidth=3, relief="raised", padding=5) # Tkinter label to show relevant info
        self.label_binding.grid(column=0, row=0, padx=5) # Position the label inside the Pollen frame
        # Create a string variable using tkinter class StringVar
        self.contents = StringVar()
        self.key_bind = StringVar()
        # Set the variable value
        self.contents.set(f"{self.famiglia}: {self.tot}")
        self.key_bind.set("")
        # Set the label above to the variable value
        self.label["textvariable"] = self.contents
        self.label_binding["textvariable"] = self.key_bind
    
    def add(self, event) -> None:
        """Callback function to increment pollen count."""
        self.tot += 1

    def update_count(self, event) -> None:
        """Callback function to update the label text."""
        self.contents.set(f"{self.famiglia}: {self.tot}")
        self.label["textvariable"] = self.contents

    @property
    def __dict__(self) -> dict:
        return {"famiglia": self.famiglia, "nome": self.nome, "conteggio": self.tot}


    @classmethod
    def generate_with_binding(cls: Pollini, master: ttk.Frame, fam: str, nome: str, key: str, count: int=0) -> Pollini:
        """Class method used to generate a new pollen instance while at the same time binding it to a keyboard key."""
        pln = cls(master, fam, nome, count) # Instantiate pollen object
        pln.master.bind(f"<{key}>", pln.add) # Bind the key to increase the pollen count
        pln.master.bind(f"<{key}>", pln.update_count, add='+') # Bind the key to also update the label value
        pln.key_bind.set(f"{key}")
        return pln


class Application():
    """Class to manage the pollen grid and placement, along with external buttons."""

    def __init__(self: Application, master: ttk.Frame, cols: int) -> None:
        self.master = master
        self.cols = cols
        self.pollens = []

        self.button_load = ttk.Button(self.master, text="Load", command=self.load) # Load button
        self.button_save = ttk.Button(self.master, text="Save", command=self.save) # Save button
        self.button_quit = ttk.Button(self.master, text="Quit", command=self.master.destroy) # Quit button
        self.id_entry = ttk.Entry(self.master)
        self.id_entry.bind("<Return>", self.focus_on_master)

    def focus_on_master(self, event):
        return self.master.focus()

    def add_pollens(self, pollens: list, bindings: list) -> None:
        """Function to generate all bindings needed for the whole app."""
        if len(pollens) != len(bindings):
            raise IndexError("The length of pollen list and bindings is not the same.")
        for i in range(len(pollens)):
            try:
                pln = Pollini.generate_with_binding(self.master, pollens[i]['famiglia'], pollens[i]['nome'], bindings[i], pollens[i]['conteggio'])
            except KeyError:
                pln = Pollini.generate_with_binding(self.master, pollens[i]['famiglia'], pollens[i]['nome'], bindings[i])
            self.pollens.append(pln)
            pln.update_count(None)

    def add_standard_pollens(self):
        self.add_pollens([{'famiglia': "Aceraceae", 'nome': "Aceraceae"}
            ,{'famiglia': "Cannabbaceae", 'nome': "Cannabbaceae"}
            ,{'famiglia': "Betulaceae", 'nome': "Betulaceae"}
            ,{'famiglia': "Alnus", 'nome': "Alnus"}
            ,{'famiglia': "Betula", 'nome': "Betula"}
            ,{'famiglia': "Chenopodiaceae/Amaranthaceae", 'nome': "Chenopodiaceae/Amaranthaceae"}
            ,{'famiglia': "Compositae", 'nome': "Ambrosia"}
            ,{'famiglia': "Compositae", 'nome': "Artemisia"}
            ,{'famiglia': "Corylaceae", 'nome': "Carpinus"}
            ,{'famiglia': "Corylaceae", 'nome': "Coryllus avellana"}
            ,{'famiglia': "Cupressaceae/Taxaceae", 'nome': "Cupressaceae/Taxaceae"}
            ,{'famiglia': "Fagaceae", 'nome': "Castanea sativa"}
            ,{'famiglia': "Fagaceae", 'nome': "Fagus sylvatica"}
            ,{'famiglia': "Fagaceae", 'nome': "Quercus"}
            ,{'famiglia': "Graminae", 'nome': "Graminae"}
            ,{'famiglia': "Oleaceae", 'nome': "Fraxinus"}
            ,{'famiglia': "Oleaceae", 'nome': "Olea"}
            ,{'famiglia': "Pinaceae", 'nome': "Pinaceae"}
            ,{'famiglia': "Plantaginaceae", 'nome': "Plantaginaceae"}
            ,{'famiglia': "Platanaceae", 'nome': "Platanaceae"}
            ,{'famiglia': "Polygonaceae", 'nome': "Polygonaceae"}
            ,{'famiglia': "Salicaceae", 'nome': "Populus"}
            ,{'famiglia': "Salicaceae", 'nome': "Salix"}
            ,{'famiglia': "Ulmaceae", 'nome': "Ulmaceae"}
            ,{'famiglia': "Uritcaceae", 'nome': "Uritcaceae"}
            ,{'famiglia': "Alternaria", 'nome': "Alternaria"}
        ],
        [
            "Up"
            ,"Down"
            ,"Left"
            ,"Right"
            ,"a"
            ,"b"
            ,"c"
            ,"d"
            ,"e"
            ,"f"
            ,"g"
            ,"h"
            ,"i"
            ,"j"
            ,"k"
            ,"l"
            ,"m"
            ,"n"
            ,"o"
            ,"p"
            ,"q"
            ,"r"
            ,"s"
            ,"t"
            ,"u"
            ,"w"
        ])

    # def add_standard_pollens(self):
    #         self.pollens = [Pollini.generate_with_binding(self.master, "Aceraceae", "Aceraceae", "Up")
    #             ,Pollini.generate_with_binding(self.master, "Cannabbaceae", "Cannabbaceae", "Down")
    #             ,Pollini.generate_with_binding(self.master, "Betulaceae", "Betulaceae", "Left")
    #             ,Pollini.generate_with_binding(self.master, "Alnus", "Alnus", "Right")
    #             ,Pollini.generate_with_binding(self.master, "Betula", "Betula", "a")
    #             ,Pollini.generate_with_binding(self.master, "Chenopodiaceae/Amaranthaceae", "Chenopodiaceae/Amaranthaceae", "b")
    #             ,Pollini.generate_with_binding(self.master, "Compositae", "Ambrosia", "c")
    #             ,Pollini.generate_with_binding(self.master, "Compositae", "Artemisia", "d")
    #             ,Pollini.generate_with_binding(self.master, "Corylaceae", "Carpinus", "e")
    #             ,Pollini.generate_with_binding(self.master, "Corylaceae", "Coryllus avellana", "f")
    #             ,Pollini.generate_with_binding(self.master, "Cupressaceae/Taxaceae", "Cupressaceae/Taxaceae", "g")
    #             ,Pollini.generate_with_binding(self.master, "Fagaceae", "Castanea sativa", "h")
    #             ,Pollini.generate_with_binding(self.master, "Fagaceae", "Fagus sylvatica", "i")
    #             ,Pollini.generate_with_binding(self.master, "Fagaceae", "Quercus", "j")
    #             ,Pollini.generate_with_binding(self.master, "Graminae", "Graminae", "k")
    #             ,Pollini.generate_with_binding(self.master, "Oleaceae", "Fraxinus", "l")
    #             ,Pollini.generate_with_binding(self.master, "Oleaceae", "Olea", "m")
    #             ,Pollini.generate_with_binding(self.master, "Pinaceae", "Pinaceae", "n")
    #             ,Pollini.generate_with_binding(self.master, "Plantaginaceae", "Plantaginaceae", "o")
    #             ,Pollini.generate_with_binding(self.master, "Platanaceae", "Platanaceae", "p")
    #             ,Pollini.generate_with_binding(self.master, "Polygonaceae", "Polygonaceae", "q")
    #             ,Pollini.generate_with_binding(self.master, "Salicaceae", "Populus", "r")
    #             ,Pollini.generate_with_binding(self.master, "Salicaceae", "Salix", "s")
    #             ,Pollini.generate_with_binding(self.master, "Ulmaceae", "Ulmaceae", "t")
    #             ,Pollini.generate_with_binding(self.master, "Uritcaceae", "Uritcaceae", "u")
    #             ,Pollini.generate_with_binding(self.master, "Alternaria", "Alternaria", "w")
    #         ]

    def draw_grid(self):
        # Place pollens in frame
        for i, pollen in enumerate(self.pollens):
            col = i%self.cols
            row = i//self.cols + 1
            pollen.grid(column=col, row=row, padx=10, pady=10)
        self.button_load.grid(column=self.cols-3, row=len(self.pollens)+1, padx=5, pady=5)
        self.button_save.grid(column=self.cols-2, row=len(self.pollens)+1, padx=5, pady=5)
        self.button_quit.grid(column=self.cols-1, row=len(self.pollens)+1, padx=5, pady=5)
        self.id_entry.grid(column=0, row=0, padx=5, pady=5)

    def save(self) -> None:
        id = self.id_entry.get()
        if id:
            df = pd.DataFrame([vars(pln) for pln in self.pollens])
            df.to_csv(f'./Vetrino_{id}.csv', sep=';', index=False)
        else:
            print("Error, id not set.")
    
    def load(self, *args, **kwargs) -> None:
        bindings = ["Up","Down","Left","Right","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","w"]
        if id:
            filename = f'./Vetrino_{self.id_entry.get()}.csv'
            df = pd.read_csv(filename, sep=';', index_col=False)
            self.pollens = []
            self.add_pollens(list(df.T.to_dict().values()), bindings)
            self.draw_grid()
        else:
            print("Error, id not set.")


def generate_frame(master):
    app = Application(master, 5)
    app.add_standard_pollens()
    app.draw_grid()
    return app