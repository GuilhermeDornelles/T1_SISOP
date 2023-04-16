import os
from parser.parser import Parser
from entities.RrScheduler import RRScheduler
from entities.SjfScheduler import SJFScheduler
from utils.config_parser import parse_config_file

def main():
	config_file = "config_SJF.json"
	#config_file = "config.json"
	script_path = os.path.abspath(__file__)
	file_path = os.path.join(os.path.dirname(script_path), config_file)

	processes_list, algorithm = parse_config_file(file_path)
	if not processes_list:
		print("Unaccepted configurations on config file. Please try again.")
		exit(1)

	print(f"Algo is {algorithm}")

	escalonador_teste = SJFScheduler(processes_list)
	escalonador_teste.schedule()

	# escalonador_teste = RRScheduler(processes_list)
	# escalonador_teste.schedule()


if __name__ == "__main__":
    main()
