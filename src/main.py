import os
from parser.parser import Parser
from utils.config_parser import parse_config_file

def main():
	config_file = "config_SJF.json"
	# config_file = "config.json"

	script_path = os.path.abspath(__file__)
	file_path = os.path.join(os.path.dirname(script_path), config_file)

	processes_list, algorithm  = parse_config_file(file_path)
	if not processes_list:
		print("Unaccepted configurations on config file. Please try again.")
		exit(1)

	print(f"Algo is {algorithm}")
	for process in processes_list:
		parser = Parser(filename=process.pcb.source_file)

		parser.parse()

		current = parser.alguma_coisa.root

		while current.next is not None:
			print(current)
			current = current.next

if __name__ == "__main__":
    main()
