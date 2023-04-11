from dataclasses import dataclass
from parser.models.Mnemonic import Mnemonic

@dataclass
class Program:
	root : Mnemonic
	data : dict[str, int]
	flags : dict[str, Mnemonic]

	def __str__(self) -> str:
		return f"root={self.root}, data={self.data}, flags{self.flags}"
