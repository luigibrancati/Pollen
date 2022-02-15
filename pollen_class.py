import logging


STANDARD_POLLENS = [
    {"famiglia": "Aceraceae", "nome": "Aceraceae", "key": "Up"},
    {"famiglia": "Cannabbaceae", "nome": "Cannabbaceae", "key": "Down"},
    {"famiglia": "Betulaceae", "nome": "Betulaceae", "key": "Left"},
    {"famiglia": "Alnus", "nome": "Alnus", "key": "Right"},
    {"famiglia": "Betula", "nome": "Betula", "key": "a"},
    {"famiglia": "Chenopodiaceae/Amaranthaceae", "nome": "Chenopodiaceae/Amaranthaceae", "key": "b"},
    {"famiglia": "Compositae", "nome": "Ambrosia", "key": "c"},
    {"famiglia": "Compositae", "nome": "Artemisia", "key": "d"},
    {"famiglia": "Corylaceae", "nome": "Carpinus", "key": "e"},
    {"famiglia": "Corylaceae", "nome": "Coryllus avellana", "key": "f"},
    {"famiglia": "Cupressaceae/Taxaceae", "nome": "Cupressaceae/Taxaceae", "key": "g"},
    {"famiglia": "Fagaceae", "nome": "Castanea sativa", "key": "h"},
    {"famiglia": "Fagaceae", "nome": "Fagus sylvatica", "key": "i"},
    {"famiglia": "Fagaceae", "nome": "Quercus", "key": "j"},
    {"famiglia": "Graminae", "nome": "Graminae", "key": "k"},
    {"famiglia": "Oleaceae", "nome": "Fraxinus", "key": "l"},
    {"famiglia": "Oleaceae", "nome": "Olea", "key": "m"},
    {"famiglia": "Pinaceae", "nome": "Pinaceae", "key": "n"},
    {"famiglia": "Plantaginaceae", "nome": "Plantaginaceae", "key": "o"},
    {"famiglia": "Platanaceae", "nome": "Platanaceae", "key": "p"},
    {"famiglia": "Polygonaceae", "nome": "Polygonaceae", "key": "q"},
    {"famiglia": "Salicaceae", "nome": "Populus", "key": "r"},
    {"famiglia": "Salicaceae", "nome": "Salix", "key": "s"},
    {"famiglia": "Ulmaceae", "nome": "Ulmaceae", "key": "t"},
    {"famiglia": "Uritcaceae", "nome": "Uritcaceae", "key": "u"},
    {"famiglia": "Alternaria", "nome": "Alternaria", "key": "v"}
]


class Pollen:
    def __init__(self, fam: str, nome: str, count: int = 0) -> None:
        # Initialize the ttk.Frame class with a master frame
        self.famiglia = fam  # Family
        self.nome = nome  # Name
        self.conteggio = count  # Total count
        logging.debug(f"Created pollen {self}")

    def add(self):
        self.conteggio += 1
        logging.debug(f"Updated pollen {self}")

    def reset(self):
        self.conteggio = 0
        logging.debug(f"Reset pollen {self}")

    def set_count(self, count: int):
        self.conteggio = count
        logging.debug(f"Set pollen {self} count to {self.conteggio}")

    def __str__(self):
        return f"""{{
            "famiglia": {self.famiglia},
            "nome": {self.nome},
            "conteggio": {self.conteggio}
        }}"""

    def short_str(self):
        return f"{self.famiglia}: {self.conteggio}"
