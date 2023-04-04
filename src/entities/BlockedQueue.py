from entities.Queue import Queue

class BlockedQueue(Queue):
    max_waiting_time: int
    
    def __init__(self, max_waiting_time=8):
        super.__init__()
        self.max_waiting_time = max_waiting_time
