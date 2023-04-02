
from entities.Process import Process


class ProcessSJF(Process):
    execution_time : int

    def __init__(self, pid : int, source_file : str, execution_time : int):
        super().__init__(pid=pid, source_file=source_file)
        self.execution_time = execution_time

    def __str__(self):
        return super().__str__() + f", execution_time={self.execution_time}"