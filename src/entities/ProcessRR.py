
from Process import Process
from enums.Priorities import Priorities


class ProcessRR(Process):
    priority : Priorities
    quantum : int

    def __init__(self, pid : int, arrival_time : int, source_file : str, priority : int, quantum : int):
        super().__init__(pid=pid, arrival_time=arrival_time, source_file=source_file)
        self.priority = Priorities(priority)
        self.quantum = quantum
    
    def get_priority_as_num(self):
        match self.priority:
            case Priorities.HIGH_PRIORITY:
                return 2
            case Priorities.MEDIUM_PRIORITY:
                return 1
            case Priorities.LOW_PRIORITY:
                return 0
        return 0
    
    def __str__(self):
        return super().__str__() + f", priority={self.priority}, quantum={self.quantum}"