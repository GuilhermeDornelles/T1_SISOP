from Scheduler import Scheduler
from entities.Queue import Queue

class RRScheduler(Scheduler):
    ready_queue : dict[str, Queue]
    blocked_queue : Queue
    

    def __init__(self):
        super.__init__()
        
    def sortByPriority():
        # TODO
        pass
    
    def switch_processes():
        pass
        # TODO
        # Quando um processo com prioridade mais alta quer executar
    
    