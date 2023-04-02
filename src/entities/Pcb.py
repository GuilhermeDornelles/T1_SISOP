from io import TextIOWrapper
from entities.enums.States import States


class PCB:
    state : States
    pid : int
    pc : int
    acc : int
    source_file : str # fiquei na duvida se deixamos aqui somente a string do path pro arquivo, ou ja o arquivo "aberto"

    def __init__(self, pid: int, source_file : str):
        self.pid = pid
        self.state = States.READY
        self.pc = 0
        self.acc = 0
        self.source_file = source_file

    def __str__(self):
        return f"PCB(pid={self.pid}, state={self.state}, source_file={self.source_file}, PC={self.pc}, acc={self.acc})"

    def update(self, new_pc : int, new_acc : int):
        self.pc = new_pc
        self.acc = new_acc