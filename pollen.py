import logging


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

    def __str__(self):
        return f"""{{
            "famiglia": {self.famiglia},
            "nome": {self.nome},
            "conteggio": {self.conteggio}
        }}"""

    def short_str(self):
        return f"{self.famiglia}: {self.conteggio}"