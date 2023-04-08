from entities.Queue import Queue
from entities.Process import Process
from entities.ProcessRR import ProcessRR
from entities.Scheduler import Scheduler
from entities.enums.Priorities import Priorities
from entities.enums.States import States

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
        self.blocked_queue = Queue()
        
    def schedule(self):
        current_processing_time = 0
        while not self.canScheduleEnd():
            current_processing_time += 1
            # Incrementamos 1 no clock
            self.incrementClock()
            # Atualizando as filas de prontos com os processos chegando (no instante de tempo atual)
            self.updateReadyQueues(curr_time=self.clock)

            if self.running_p is None: # vai cair aqui se for a primeira iteracao, ou o ultimo running_p foi pra exit
                self.running_p = self.switch_processes()
                current_processing_time = 1
            elif self.existHigherPriorityProcessReady() or (current_processing_time > self.running_p.quantum):
                # TODO logica de manter o new_pc e new_acc no loop pra atualizar a PCB desse running_p antes de trocar
                self.running_p.pcb.update(new_pc=None, new_acc=None, new_state=States.READY)
                self.running_p = self.switch_processes()
                current_processing_time = 1
            # else:
                # se o mesmo processo continuar com o escalonador, roda normal

            # TODO definir como vamos executar uma instrução desse P
            # abrir o arquivo fonte
            # executar a instrucao que está no PC
            # se instrucao for I/O SYSCANLL 1 ou 2
                # faz o I/O, atualizando o acc
                # manda P pra fila de bloqueados (setando nele o time_to_wait)
                # atualizar o acc (com base na instrucao)

            
            # se instrucaso for SYSCALL 0,
            self.exitProcess(self.running_p)
            self.running_p = None


    def updateReadyQueues(self, curr_time : int):
        arriving_processes = self.getArrivingProcesses()
        for process in arriving_processes:
            process.pcb.initProcess(curr_time)
            if process.priority == Priorities.HIGH_PRIORITY:
                self.HP_ready_queue.push(process)
            elif process.priority == Priorities.MEDIUM_PRIORITY:
                self.MP_ready_queue.push(process)
            elif process.prioriry == Priorities.LOW_PRIORITY:
                self.LP_ready_queue.push(process)

    def existHigherPriorityProcessReady(self) -> bool:
        current_priority = self.running_p.priority
        if current_priority != Priorities.HIGH_PRIORITY and not self.HP_ready_queue.isEmpty():
            return True
        elif current_priority == Priorities.LOW_PRIORITY and not self.MP_ready_queue.isEmpty():
            return True

        # se chegar aqui é pq current é LP, ou HP, ou MP com HP vazio
        return False


    def switch_processes(self) -> ProcessRR:
        # Retorna o proximo processo que deve executar
        if not self.HP_ready_queue.isEmpty():
            return self.HP_ready_queue.pop()
        elif not self.MP_ready_queue.isEmpty():
            return self.MP_ready_queue.pop()
        elif not self.LP_ready_queue.isEmpty():
            return self.LP_ready_queue.pop()
        else:
            # Se chegarmos aqui é pq nao existe nenhum P pronto
            # TODO definir o que acontece nesse caso
            return None
        
    
    