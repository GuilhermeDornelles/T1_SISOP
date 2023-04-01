from src.entities.PCB import PCB
from src.entities.enums.Priorities import Priorities


class Process:
    waiting_time : int
    processing_time : int
    arrival_time : int
    pcb : PCB

    def __init__(self, pid, source_file):
        self.pcb = PCB(pid, source_file)
