from entities.BlockedQueue import BlockedQueue
from entities.ReadyQueue import ReadyQueue

class Scheduler:
    blocked_queue: BlockedQueue
    ready_queue: ReadyQueue
    
    def __init__(self):
        self.blocked_queue = BlockedQueue()
        self.ready_queue = ReadyQueue()
        
    def switch_processes(): 
        pass
    
    def create_process():
        pass