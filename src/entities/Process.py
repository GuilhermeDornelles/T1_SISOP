from entities.Pcb import PCB


class Process:
    arrival_time : int
    pcb : PCB

    def __init__(self, pid : int, arrival_time : int, source_file : str):
        self.arrival_time = arrival_time
        self.pcb = PCB(pid, source_file)

    def __str__(self):
        return f"Process(arrival_time={self.arrival_time}, PCB=({self.pcb}))"
