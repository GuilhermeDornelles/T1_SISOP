from typing import List

from Scheduler import Scheduler
from .ProcessSJF import ProcessSJF
from .Context import Context
from .enums.States import States
from .enums.ReturnCode import ReturnCode

class SJFScheduler(Scheduler):
 
    def __init__(self, processes: List[ProcessSJF]):
        super.__init__(processes=processes)
        self.running_p: ProcessSJF = None
        self.ready_queue: List[ProcessSJF] = []
        self.blocked_queue: List[ProcessSJF] = []

    @property
    def exist_process_with_lower_execution_time(self):
        if self.running_p is None: 
            return True
        for process in self.ready_queue:
            if process.execution_time < self.running_p.execution_time:
                return True
        return False

    def schedule(self):
        acc = 0
        pc = None

        while not self.can_schedule_end:
            # TROCA DE CONTEXTO DE PROCESSO
            self.increment_clock()

            self._update_ready_queue()

            self.running_p = self.ready_queue.pop(0)
            
            acc = self.running_p.pcb.acc
            pc = self.running_p.pcb.pc
            data = self.running_p.pcb.program.data.copy()
            flags = self.running_p.pcb.program.flags

            current_processing_time = 0

            # EXECUÇÃO DO PROCESSO
            while not self.exist_process_with_lower_execution_time:
                
                context = Context(
                    pc=pc,
                    acc=acc,
                    data=data,
                    flags=flags
                )
                result = pc.function(context)

                acc = context.acc
                pc = context.pc

                self.increment_clock()
                current_processing_time+=1
                self._update_ready_queue()

                if result is not None:
                    if result == ReturnCode.EXIT:
                        self.exit_list.append(self.running_p)
                    if result in [ReturnCode.INPUT, ReturnCode.OUTPUT]:
                        break
                
            # Bloqueia processo
            self.running_p.pcb.state = States.BLOCKED
            self.blocked_queue.append(self.running_p)

            # Atualiza contexto de execução na PCB
            self.running_p.pcb.acc = acc
            self.running_p.pcb.acc = pc
            self.running_p.pcb.program.data = data

            self.running_p = None

            
    def _update_ready_queue(self):
        arriving_processes = self.get_arriving_processes()
        for process in arriving_processes:
            process.pcb.init_process(self.clock)
            self.ready_queue.append(process)

        self.ready_queue.sort(key = lambda p: p.execution_time)
