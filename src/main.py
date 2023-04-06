from parser.parser import Parser
from entities.utils.config_parser import parse_config_file

def main():

	# processes_list, algorithm = parse_config_file("config.json")
	processes_list, algorithm  = parse_config_file("config_SJF.json")
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
