from enum import Enum

class States(Enum):
    READY = 0
    RUNNING = 1
    BLOCKED = 2
    EXIT = 3