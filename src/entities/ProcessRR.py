
from src.entities.Process import Process
from src.entities.enums.Priorities import Priorities


class ProcessRR(Process):
    priority : Priorities
    quantum : int

    def __init__(self, priority, quantum):
        super().__init__()
        self.priority = priority
        self.quantum = quantum
