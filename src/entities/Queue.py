from entities.Process import Process


class Queue:
    processes: list[Process]
    
    def __init__(self):
        self.processes = []
            
    def is_empty(self) -> bool:
        return len(self.processes) == 0

    def push(self, process : Process):
        self.processes.append(process)

    def pop(self) -> Process:
        return self.processes.pop(0)
    
    def check_first(self) -> Process:
        if self.processes[0]:
            return self.processes[0]
        else:
            return None

    def sort_blocked_queue_by_priority(self):
        self.processes.sort(key = lambda process: (-process.get_priority_as_num(), process.pcb.time_to_wait))