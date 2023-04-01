from typing import Callable
from dataclasses import dataclass

@dataclass
class Mnemonic:
    name: str
    value: str
    function: Callable
    next: 'Mnemonic'

    def __str__(self):
        return f'{self.name} {self.value}'