import random
from time import sleep
from entities.Queue import Queue
from entities.Process import Process
from entities.ProcessRR import ProcessRR
from entities.Scheduler import Scheduler
from entities.enums.Priorities import Priorities
from entities.enums.States import States
from entities.Context import Context
from entities.enums.ReturnCode import ReturnCode
from utils.utils import super_print

class RRScheduler(Scheduler):
    # Cada uma dessas é a fila de prontos separada pro prioridade; quem vai gerenciar elas vai ser o escalonador dai
    HP_ready_queue : Queue #HighPriority
    MP_ready_queue : Queue #MediumPriority
    LP_ready_queue : Queue #LowPriority
    blocked_queue : Queue
    running_p : ProcessRR
    
    def __init__(self, processes : list[Process]):
        super().__init__(processes=processes)
        self.running_p = None
        self.HP_ready_queue = Queue()
        self.MP_ready_queue = Queue()
        self.LP_ready_queue = Queue()
        # TODO botar essa fila no Scheduler, pq pode ser usada no SJF tambem
        self.blocked_queue = Queue()
        
    def schedule(self):
        current_processing_time = 0
        current_pc = None
        current_acc = 0

        while not self.can_schedule_end:
            current_processing_time += 1
            self.increment_clock()
            super_print(f"TIME {self.clock}")
            # Atualizando as filas de prontos com os novos processos chegando (no instante de tempo atual)
            self.update_ready_queues(curr_time=self.clock)
            self.update_blocked_queue(curr_time=self.clock)

            if self.running_p is None or (not self.running_p.pcb.is_ready() and not self.running_p.pcb.is_running() or self.running_p.pcb.is_exited()): # vai cair aqui se for a primeira iteracao, ou o ultimo running_p foi pra exit ou pra blocked
                new_p = self.switch_processes()
                if not new_p:
                    print("nenhum P novo, nada para escalonar: ", new_p)
                    continue
                current_pc, current_acc = self.schedule_process(new_p, self.clock)
                current_processing_time = 1

            elif self.exist_higher_priority_process_ready():
                self.running_p.pcb.update(new_pc=current_pc, new_acc=current_acc, instant_time=self.clock, new_state=States.READY)
                self._add_to_proper_ready_queue(self.running_p)
                new_p = self.switch_processes()
                print(f"P com prioridade escalonado PID={new_p.pcb.pid}")
                if not new_p:
                    print("nenhum P novo, nada para escalonar: ", new_p)
                    continue
                current_pc, current_acc = self.schedule_process(new_p, self.clock)
                current_processing_time = 1

            elif (current_processing_time > self.running_p.quantum):
                print(f"Chegou no limite do quantum = {current_processing_time}")
                self.running_p.pcb.update(new_pc=current_pc, new_acc=current_acc, instant_time=self.clock, new_state=States.READY)
                new_p = self.switch_processes()
                if not new_p:
                    print("nenhum P novo, nada para escalonar: ", new_p)

                    continue
                current_pc, current_acc = self.schedule_process(new_p, self.clock)
                current_processing_time = 1

            data = Context(
                        pc=current_pc,
                        acc=current_acc,
                        data=self.running_p.pcb.program.data,
                        flags=self.running_p.pcb.program.flags
                    )
            return_type = current_pc.function(data)

            current_acc = data.acc
            print(f'Process PID={self.running_p.pcb.pid} with PC = {current_pc}')
            current_pc = data.pc
            
            if return_type is not None:
                if return_type == ReturnCode.EXIT:
                    self.exit_process(self.running_p)
                    self.running_p = None
                elif return_type == ReturnCode.OUTPUT or return_type == ReturnCode.INPUT:
                    self.running_p.pcb.update(new_pc=current_pc, new_acc=current_acc, instant_time=self.clock, new_state=States.BLOCKED)
                    self.block_process(process=self.running_p, curr_time=self.clock)
                    self.running_p = None

    def unblock_process(self, process: Process, curr_time : int):
        process.pcb.unblock_process(instant_time=curr_time)
        self.blocked_queue.processes.remove(process)
        self._add_to_proper_ready_queue(process)

    def block_process(self, process: Process, curr_time : int):
        time = random.randint(8, 10)
        super_print(f"Time to wait de PID {process.pcb.pid} = {time}")
        process.pcb.block_process(instant_time=curr_time, time_to_wait=time)
        self.blocked_queue.push(process)
        if(process in self.HP_ready_queue.processes):
            self.HP_ready_queue.processes.remove(process)
            
        elif(process in self.MP_ready_queue.processes):
            self.MP_ready_queue.processes.remove(process)
            
        elif(process in self.LP_ready_queue.processes):
            self.LP_ready_queue.processes.remove(process)

    def update_blocked_queue(self, curr_time):
        self.blocked_queue.sort_blocked_queue_by_priority()
        for process in self.blocked_queue.processes:
            if process.pcb.time_to_wait > 0:
                process.pcb.decrease_time_to_wait()
            else:
                print(f'Unblock process pid={process.pcb.pid}')
                self.unblock_process(process, curr_time)
                
    def update_ready_queues(self, curr_time : int):
        arriving_processes = self.get_arriving_processes()
        for process in arriving_processes:
            process.pcb.init_process(curr_time)
            self._add_to_proper_ready_queue(process)

    def exist_higher_priority_process_ready(self) -> bool:
        current_priority = self.running_p.priority
        if current_priority != Priorities.HIGH and not self.HP_ready_queue.is_empty():
            return True
        elif current_priority == Priorities.LOW and not self.MP_ready_queue.is_empty():
            return True
        # se chegar aqui é pq current é LP com HP e MP vazios, ou HP, ou MP com HP vazio
        return False

    def switch_processes(self) -> ProcessRR:
        # Retorna o proximo processo que deve executar
        if not self.HP_ready_queue.is_empty():
            print(f'SWITCHING PROCESS')
            return self.HP_ready_queue.pop()
        elif not self.MP_ready_queue.is_empty():
            print(f'SWITCHING PROCESS')
            return self.MP_ready_queue.pop()
        elif not self.LP_ready_queue.is_empty():
            print(f'SWITCHING PROCESS')
            return self.LP_ready_queue.pop()
        else:
            # Se chegarmos aqui é pq nao existe nenhum P pronto
            return None

    def _add_to_proper_ready_queue(self, process : Process):
        if process.priority == Priorities.HIGH:
            self.HP_ready_queue.push(process)
        elif process.priority == Priorities.MEDIUM:
            self.MP_ready_queue.push(process)
        elif process.priority == Priorities.LOW:
            self.LP_ready_queue.push(process)
