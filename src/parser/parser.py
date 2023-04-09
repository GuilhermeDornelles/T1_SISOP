from .models.Program import Program
from .models.Mnemonic import Mnemonic
from .constants import constants


class Parser:
     
	def __init__(self, filename: str):
		self.filename = filename
		self.program = None
	
	def parse(self):
		self.program = Program()
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
						self.program.flags[line[0]] = None
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
						self.program.pc = mnemonic
					else:
						last.next = mnemonic

					if flag:
						self.program.flags[flag] = mnemonic
						flag = False

					last = mnemonic
					i+=1
					line = lines[i].strip()
					
			if line == '.data':
				i+=1
				line = lines[i].strip()
				while line != '.enddata':
					variable_name = line.split(' ')[0]
					variable_value = line.split(' ')[1]
					self.program.data[variable_name] = variable_value

			i+=1

		return self.program
					
	@staticmethod
	def _read_file_in_lines(filename: str):
		with open(filename, 'r') as file:
			lines = file.readlines()
		return lines
	