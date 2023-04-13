from dataclasses import dataclass
from parser.models.Mnemonic import Mnemonic

@dataclass
class InstructionData:
    pc : Mnemonic
    acc : int
    data : dict[str, int]
    flags : dict[str, Mnemonic]
