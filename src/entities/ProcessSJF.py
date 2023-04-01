
from src.entities.Process import Process


class ProcessSJF(Process):
    execution_time : int

    def __init__(self):
        super().__init__()