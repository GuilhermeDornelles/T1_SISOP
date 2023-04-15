import random
from entities.Queue import Queue
from entities.Process import Process
from entities.ProcessRR import ProcessRR
from entities.Scheduler import Scheduler
from entities.enums.Priorities import Priorities
from entities.enums.States import States
from entities.InstructionData import InstructionData
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
        pc_atual = None
        acc_atual = 0
        while not self.can_schedule_end():
            current_processing_time += 1
            # Incrementamos 1 no clock
            self.increment_clock()
            super_print(f"TIME {self.clock}")
            # Atualizando as filas de prontos com os novos processos chegando (no instante de tempo atual)
            self.update_ready_queues(curr_time=self.clock)

            self.update_blocked_queue(curr_time=self.clock)

            if self.running_p is None: # vai cair aqui se for a primeira iteracao, ou o ultimo running_p foi pra exit
                new_p = self.switch_processes()
                if not new_p:
                    print("nenhum P novo, nada para escalonar: ", new_p)
                    continue
                self.running_p = new_p
                super_print(f"ESCALONOU P com ID: {self.running_p.pcb.pid}")
                current_processing_time = 1
                acc_atual = self.running_p.pcb.acc
                pc_atual = self.running_p.pcb.pc
            elif self.exist_higher_priority_process_ready() or (current_processing_time > self.running_p.quantum):
                self.running_p.pcb.update(new_pc=pc_atual, new_acc=acc_atual, instant_time=self.clock, new_state=States.READY)
                self.running_p = self.switch_processes()
                super_print(f"ESCALONOU P com ID: {self.running_p.pcb.pid}")
                current_processing_time = 1
                pc_atual = self.running_p.pcb.pc
                acc_atual = self.running_p.pcb.acc
            # TODO testar toda essa parte da logica abaixo, ate o fim do schedule()
            print(f"ACC atual: {acc_atual} PC atual: {pc_atual}")
            data = InstructionData(
                        pc=pc_atual,
                        acc=acc_atual,
                        data=self.running_p.pcb.program.data,
                        flags=self.running_p.pcb.program.flags
                    )
            return_type = pc_atual.function(data)

            pc_atual = data.pc
            acc_atual = data.acc
            
            if return_type and return_type == ReturnCode.EXIT:
                # se instrucao for SYSCALL 0
                # TODO comandos pra printar os stats do Processo quando ele vai pra exit
                # chamar o time_stats da PCB do processo
                super_print(f"EXITING P ID: {self.running_p.pcb.pid}")
                super_print(self.running_p.pcb.time_stats.final_times())
                self.exit_process(self.running_p)
                self.running_p = None
            elif return_type and (return_type == ReturnCode.OUTPUT or return_type == ReturnCode.INPUT):
                self.running_p.pcb.update(new_pc=pc_atual, new_acc=acc_atual, instant_time=self.clock, new_state=States.BLOCKED)
                self.block_process(process=self.running_p, curr_time=self.clock)
    
    def unblock_process(self, process: Process, curr_time : int):
        process.pcb.unblock_process(instant_time=curr_time)
        self._add_to_proper_ready_queue(process)

    def block_process(self, process: Process, curr_time : int):
        time = random.randint(8, 10)
        process.pcb.block_process(instant_time=curr_time, time_to_wait=time)
        self.blocked_queue.push(process)

    def update_blocked_queue(self, curr_time):
        self.blocked_queue.sort_blocked_queue_by_priority()
        for process in self.blocked_queue.processes:
            if(process.pcb.time_to_wait > 0):
                process.pcb.decrease_time_to_wait()
            else:
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
            return self.HP_ready_queue.pop()
        elif not self.MP_ready_queue.is_empty():
            return self.MP_ready_queue.pop()
        elif not self.LP_ready_queue.is_empty():
            return self.LP_ready_queue.pop()
        else:
            # Se chegarmos aqui é pq nao existe nenhum P pronto
            # TODO definir o que acontece nesse caso
            return None
    
    def _add_to_proper_ready_queue(self, process : Process):
        if process.priority == Priorities.HIGH:
            self.HP_ready_queue.push(process)
        elif process.priority == Priorities.MEDIUM:
            self.MP_ready_queue.push(process)
        elif process.prioriry == Priorities.LOW:
            self.LP_ready_queue.push(process)
