from entities.Process import Process

class Scheduler:
    # Instante de tempo atual
    clock : int
    # Lista Constante de todos os processos
    all_processes_list : list[Process]
    # Lista dos processos que ainda faltam "chegar"
    processes_to_arrive : list[Process]
    exit_list : list[Process]
    
    def __init__(self, processes : list[Process]):
        self.clock = -1
        processes.sort(key = lambda p : p.arrival_time)
        self.all_processes_list = processes
        self.processes_to_arrive = processes
        self.exit_list = []

    def increment_clock(self):
        self.clock += 1

    def get_arriving_processes(self) -> list[Process]:
        arriving_processes = []
        temp_list = self.processes_to_arrive
        for process in temp_list:
            if process.arrival_time <= self.clock:
                arriving_processes.append(process)
                self.processes_to_arrive.remove(process)
            else:
                return arriving_processes
        return arriving_processes
    
    def exit_process(self, process : Process):
        self.exit_list.append(process)

    def can_schedule_end(self) -> bool:
        return len(self.all_processes_list) == len(self.exit_list)
