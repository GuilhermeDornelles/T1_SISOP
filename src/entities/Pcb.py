from io import TextIOWrapper
from src.entities.enums.States import States


class PCB:
    state : States
    pid : int
    pc : int
    acc : int
    source_file : TextIOWrapper # fiquei na duvida se deixamos aqui somente a string do path pro arquivo, ou ja o arquivo "aberto"

    def __init__(self, pid: int, source_file : TextIOWrapper):
        self.pid = pid
        self.pc = 0
        self.acc = 0
        self.source_file = source_file

    def update(self, new_pc : int, new_acc : int):
        self.pc = new_pc
        self.acc = new_acc