from entities.Process import Process

class Queue:
    processes: Process[0]
    
    def __init__(self):
        self.processes = []