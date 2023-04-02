import json
from parser.parser import Parser
from entities.Process import Process
from entities.ProcessRR import ProcessRR
from entities.ProcessSJF import ProcessSJF

def parse_config_file(config_file : str) -> tuple[list[Process], str]:
	with open(config_file) as config:
		data = json.load(config)

	algorithm : str = data.get("algorithm")
	if algorithm not in ["RR", "SJF"]:
		print("Please provide a valid algorithm name on the config. Options: [RR / SJF]")
		return None, None
	processes_raw = data.get('processes')
	if not processes_raw:
		print("Please provide at least one process to execute.")
		return None, algorithm

	processes_list : list[Process] = []
	for process in processes_raw:
		pid = process.get("pid")
		file = process.get("source_file")
		if algorithm == "RR":
			new_process = ProcessRR(pid=pid, source_file=file, quantum=process.get("quantum"), priority=process.get("priority"))
		elif algorithm == "SJF":
			new_process = ProcessSJF(pid=pid, source_file=file, execution_time=process.get("execution_time"))
		processes_list.append(new_process)

	return processes_list, algorithm

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
