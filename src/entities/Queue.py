from entities.Process import Process

class Queue:
    processes: list[Process]
    
    def __init__(self):
        self.processes = []