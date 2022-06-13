import logging


custom_logger = logging.getLogger(name="pollen_logger")


class Pollen:
    def __init__(
        self, famiglia: str, nome: str, use_family: bool, conteggio: int = 0
    ) -> None:
        # Initialize the ttk.Frame class with a master frame
        self.famiglia = famiglia  # Family
        self.nome = nome  # Name
        self.conteggio = conteggio  # Total count
        self.use_family = use_family  # Use family or name in the frontend
        custom_logger.debug(f"Created pollen {self}")

    def add(self):
        self.conteggio += 1
        custom_logger.debug(f"Updated pollen {self}")

    def reset(self):
        self.conteggio = 0
        custom_logger.debug(f"Reset pollen {self}")

    def set_count(self, count: int):
        self.conteggio = count
        custom_logger.debug(f"Set pollen {self} count to {self.conteggio}")

    def __str__(self):
        return f"""{{
            "famiglia": {self.famiglia},
            "nome": {self.nome},
            "conteggio": {self.conteggio}
        }}"""

    def short_str(self):
        return (
            f"{self.famiglia}: {self.conteggio}"
            if self.use_family
            else f"{self.nome}: {self.conteggio}"
        )
