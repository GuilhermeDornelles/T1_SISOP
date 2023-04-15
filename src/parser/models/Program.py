from dataclasses import dataclass
from parser.models.Mnemonic import Mnemonic

@dataclass
class Program:
	root : Mnemonic
	data : dict[str, int]
	flags : dict[str, Mnemonic]

	def __init__(self):
		self.root = None
		self.data = dict()
		self.flags = dict()

	def __str__(self) -> str:
		return f"root={self.root}, data={self.data}, flags=''"
