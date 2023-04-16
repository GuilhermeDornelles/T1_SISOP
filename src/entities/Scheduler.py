from entities.Process import Process
from entities.enums.States import States
from utils.utils import super_print

class Scheduler:
    # Instante de tempo atual
    clock : int
    # Lista Constante de todos os processos
    all_processes_list : list[Process]
    # Lista dos processos que ainda faltam "chegar"
    processes_to_arrive : list[Process]
    exit_list : list[Process]
    running_p : Process
    
    def __init__(self, processes : list[Process]):
        self.clock = -1
        processes.sort(key = lambda p : p.arrival_time)
        self.all_processes_list = processes
        self.processes_to_arrive = processes
        self.exit_list = []
        self.running_p = None

    @property
    def can_schedule_end(self) -> bool:
        return len(self.all_processes_list) == len(self.exit_list)

    def increment_clock(self):
        self.clock += 1

    def get_arriving_processes(self) -> list[Process]:
        curr_arriving = []
        temp_list = self.processes_to_arrive
        for process in temp_list:
            if process.arrival_time <= self.clock:
                curr_arriving.append(process)
                self.processes_to_arrive.remove(process)
            else:
                return curr_arriving
        return curr_arriving

    def schedule_process(self, process : Process, instant_time : int):
        if process:
            self.running_p = process
            process.pcb.update(new_pc=process.pcb.pc, new_acc=process.pcb.acc, instant_time=instant_time, new_state=States.RUNNING)
            super_print(f"ESCALONOU P com ID: {self.running_p.pcb.pid}")

    def exit_process(self, process : Process):
        process.pcb.update(new_pc=process.pcb.pc, new_acc=process.pcb.acc, instant_time=self.clock, new_state=States.EXIT)
        super_print(f"EXITING P ID: {process.pcb.pid}")
        super_print(process.pcb.time_stats.final_times())
        self.exit_list.append(process)

    
