from .models.Mnemonic import Mnemonic
from .constants import constants

class AlgumaCoisa:
    
	def __init__(self):
		self.root = None
		self.data = {}
		self.flags = {}

class Parser:
     
	def __init__(self, filename: str):
		self.filename = filename
		self.alguma_coisa = None
	
	def parse(self):
		self.alguma_coisa = AlgumaCoisa()
		lines = Parser._read_file_in_lines(self.filename)

		last = None
		flag = False
		for i in range(len(lines)):
			line = lines[i].strip()

			if line == '.code':
				i+=1
				line = lines[i].strip()
				while line != '.endcode':

					if ':' in line:
						line = line.split(':')
						self.alguma_coisa.flags[line[0]] = None
						flag = line[0]
					else:
						# caso for comando normal
						cmd_name = line.split(' ')[0].upper()
						cmd_value = line.split(' ')[1]
						cmd_func = constants[cmd_name]
						mnemonic = Mnemonic(
							name=cmd_name,
							value=cmd_value, 
							function=cmd_func,
							next=None
						)

					if last is None:
						self.alguma_coisa.root = mnemonic
					else:
						last.next = mnemonic

					if flag:
						self.alguma_coisa.flags[flag] = mnemonic
						flag = False

					last = mnemonic
					i+=1
					line = lines[i].strip()
			i+=1
					
	@staticmethod
	def _read_file_in_lines(filename: str):
		with open(filename, 'r') as file:
			lines = file.readlines()
		return lines
	