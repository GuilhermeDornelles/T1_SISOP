from entities.Process import Process

class Queue:
    processes: list[Process]
    
    def __init__(self):
        self.processes = []

    def isEmpty(self) -> bool:
        return len(self.processes) == 0

    def push(self, process : Process):
        self.processes.append(process)

    def pop(self) -> Process:
        return self.processes.pop(0)