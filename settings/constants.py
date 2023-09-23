from enum import Enum


class Lang(str, Enum):
    EN: str = "en"
    DE: str = "de"

    def __str__(self):
        return self.value


class Template(str, Enum):
    BASE: str = "base"
    XTND: str = "Xtnd"

    def __str__(self):
        return self.value
