import json
from parser.parser import Parser
from src.entities.ProcessRR import ProcessRR
from src.entities.enums.Priorities import Priorities


def main():
	# parser = Parser('./src/tests/prog1.txt')

	# parser.parse()

	# current = parser.alguma_coisa.root

	# while current.next is not None:
	# 	print(current)
	# 	current = current.next

	with open("config.json") as config_file:
		data = json.load(config_file)
		
	algorithm = data.get("algorithm")
	if algorithm not in ["RR", "SJF"]:
		print("Please provide a valid algorithm name on the config. Options: [RR / SJF]")
		exit(1)
	
	processes_list = data.get('processes')
	if not processes_list:
		print("Please provide at least one process to execute.")
		exit(1)

	processes = []
	for process in processes_list:
		if algorithm is "RR":
			priority = Priorities(process.get("priority"))
			new_process = ProcessRR(process.get("pid"), process.get("source_file"), process.get("quantum"), priority)
		processes.append(new_process)

	print(processes)
if __name__ == "__main__":
    main()