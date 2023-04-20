import random
from typing import List

from .Scheduler import Scheduler
from .ProcessSJF import ProcessSJF
from .Context import Context
from .enums.States import States
from .enums.ReturnCode import ReturnCode

class SJFScheduler(Scheduler):
 
    def __init__(self, processes: List[ProcessSJF]):
        super().__init__(processes=processes)
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

    def increment_clock(self):
        res = super().increment_clock()
        print(f'\n## time {self.clock} ##')
        return res

    def schedule(self):
        acc = 0
        pc = None
        is_swaping_context = False

        while not self.can_schedule_end:
            # TROCA DE CONTEXTO DE PROCESSO
            if not is_swaping_context:
                self.increment_clock()
            is_swaping_context = False

            self._update_blocked_queue()
            self._update_ready_queue()

            if len(self.ready_queue) > 0:
                self.running_p = self.ready_queue.pop(0)
                self.running_p.pcb.update_state(self.clock, States.RUNNING)
                print(f'(scheduled process) pid={self.running_p.pcb.pid}')
                
                acc = self.running_p.pcb.acc
                pc = self.running_p.pcb.pc
                data = self.running_p.pcb.program.data.copy()
                flags = self.running_p.pcb.program.flags

                current_processing_time = 0

                # EXECUÇÃO DO PROCESSO
                while not self.exist_process_with_lower_execution_time:
                    print(f'(executing) process pid={self.running_p.pcb.pid}')

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
                    self._update_blocked_queue()
                    self._update_ready_queue()

                    if result is not None:
                        break
                    result = None
                        
                if result == ReturnCode.EXIT:
                    print(f'(exiting process) pid={self.running_p.pcb.pid}')
                    self.exit_list.append(self.running_p)
                    self.running_p.pcb.update_state(self.clock, States.EXIT)
                    print(f"ACC final => {self.running_p.pcb.acc}")
                    print(self.running_p.pcb.time_stats.final_times())
                if result in [ReturnCode.INPUT, ReturnCode.OUTPUT]:
                    # Bloqueia processo
                    print(f'(blocking process) pid={self.running_p.pcb.pid}')
                    time_to_wait = random.randint(8, 10)
                    self.running_p.pcb.block_process(self.clock, time_to_wait)
                    self.blocked_queue.append(self.running_p)
                if result is None:
                    self.running_p.pcb.update_state(self.clock, States.READY)
                    self.ready_queue.append(self.running_p)
                    
                # Atualiza contexto de execução na PCB
                self.running_p.pcb.acc = acc
                self.running_p.pcb.pc = pc
                self.running_p.pcb.program.data = data

                is_swaping_context = True
                self.running_p = None
            else:
                print(f'nothing to run.')

    def _update_blocked_queue(self):
        for process in self.blocked_queue:
            if process.pcb.time_to_wait > 0:
                process.pcb.decrease_time_to_wait()
            else:
                print(f'(process gone ready) pid={process.pcb.pid}')
                process.pcb.unblock_process(self.clock)
                self.blocked_queue.remove(process)
                self.ready_queue.append(process)

    def _update_ready_queue(self):
        arriving_processes = self.get_arriving_processes()
        for process in arriving_processes:
            print(f'(process arrived) pid={process.pcb.pid}')
            process.pcb.init_process(self.clock)
            self.ready_queue.append(process)

        self.ready_queue.sort(key = lambda p: p.execution_time)
