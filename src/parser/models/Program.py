from dataclasses import dataclass
from parser.models.Mnemonic import Mnemonic

@dataclass
class Program:
    
	pc : Mnemonic
	acc : int
	data : dict[str, int]
	flags : dict[str, Mnemonic]

	def __init__(self):
		self.pc = None
		self.acc = None
		self.data = {}
		self.flags = {}

	def step(self):
		# Executa a proxima função do programa
		# A propria função já altera pc para o proximo comando
		self.pc.run(self)
		print(self)

	def __str__(self) -> str:
		return f"pc={self.pc}, acc={self.acc}, data={self.data}, flags{self.flags}"
