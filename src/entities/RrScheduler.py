from Scheduler import Scheduler
from entities.Queue import Queue
from entities.Process import Process
from entities.ProcessRR import ProcessRR
from entities.enums.Priorities import Priorities

class RRScheduler(Scheduler):
    # Cada uma dessas é a fila de prontos separada pro prioridade; quem vai gerenciar elas vai ser o escalonador dai
    HP_ready_queue : Queue #HighPriority
    MP_ready_queue : Queue #MediumPriority
    LP_ready_queue : Queue #LowPriority
    blocked_queue : Queue
    running_p : Process
    exit_list : list[ProcessRR]
    
    def __init__(self):
        super.__init__()
        
    def schedule(self, processes : list[ProcessRR]):
        for process in processes:
            if process.priority == Priorities.HIGH_PRIORITY:
                self.HP_ready_queue.push(process)
            elif process.priority == Priorities.MEDIUM_PRIORITY:
                self.MP_ready_queue.push(process)
            elif process.prioriry == Priorities.LOW_PRIORITY:
                self.LP_ready_queue.push(process)

        running_p = self.switch_processes()
        # TODO definir como vamos executar uma instrução desse P


    def sortByPriority():
        # TODO
        pass
    
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
        
    
    