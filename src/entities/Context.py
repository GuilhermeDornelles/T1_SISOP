from dataclasses import dataclass
from parser.models.Mnemonic import Mnemonic

@dataclass
class Context:
    pc : Mnemonic
    acc : int
    data : dict[str, int]
    flags : dict[str, Mnemonic]

    def __str__(self):
        return f'pc={self.pc}, acc={self.acc}, data={self.data}, flags={self.flags}'