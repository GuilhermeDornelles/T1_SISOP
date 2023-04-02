from entities.PCB import PCB
from entities.enums.Priorities import Priorities


class Process:
    waiting_time : int
    processing_time : int
    arrival_time : int
    pcb : PCB

    def __init__(self, pid: int, source_file: str):
        self.pcb = PCB(pid, source_file)
    
    def __str__(self):
        return f"Process(PCB={self.pcb})"
