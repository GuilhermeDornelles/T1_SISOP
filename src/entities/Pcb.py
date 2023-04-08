from enums.States import States
from TimespentStats import TimespentStats


class PCB:
    state : States
    pid : int
    pc : int
    acc : int
    source_file : str # fiquei na duvida se deixamos aqui somente a string do path pro arquivo, ou ja o arquivo "aberto"
    time_to_wait: int
    time_stats = TimespentStats

    def __init__(self, pid: int, source_file : str):
        self.pid = pid
        self.source_file = source_file
        self.time_stats = TimespentStats()
        self.state = None
        self.pc = 0
        self.acc = 0
        self.time_to_wait = 0

    def __str__(self):
        return f"PCB(pid={self.pid}, state={self.state}, source_file={self.source_file}, PC={self.pc}, acc={self.acc})"
    
    def initProcess(self, instant_time : int):
        self._initState(States.READY, instant_time)

    def blockProcess(self, instant_time, time_to_wait=8):
        self.time_to_wait = time_to_wait
        self._updateState(States.BLOCKED, instant_time)
        # TODO: Ver o que mais vai acontecer quando um processo for bloqueado

    def unblockProcess(self, new_state=States.READY):
        self.time_to_wait = 0
        # Novo estado pode ser READY, ou outro; por isso pode receber por parametro
        self._updateState(new_state)
        # TODO: Ver o que mais vai acontecer quando um processo for desbloqueado

    def decreaseWaintingTime(self):
        self.time_to_wait -= 1

    def update(self, new_pc : int, new_acc : int, new_state = States.READY):
        self.pc = new_pc
        self.acc = new_acc
        self._updateState(new_state)

    def _initState(self, new_state : States, instant_time : int):
        if self.state is None:
            self.time_stats.addTimeEnterReady(time=instant_time)
            self.state = States.READY
        else:
            self._updateState(new_state, instant_time)

    def _updateState(self, new_state : States, instant_time : int):
        if new_state == States.BLOCKED:
            # P ta saindo de RUNNING e entrando em BLOCKED
            self.time_stats.addTimeExitRunning(time=instant_time)
            self.time_stats.addTimeEnterBlocked(time=instant_time)

        elif new_state == States.READY:
            # P ta saindo ou de BLOCKED ou de RUNNING e entrando em READY
            if self.state == States.BLOCKED:
                self.time_stats.addTimeExitBlocked(time=instant_time)
            elif self.state == States.RUNNING:
                self.time_stats.addTimeExitRunning(time=instant_time)

            self.time_stats.addTimeEnterReady(time=instant_time)

        elif new_state == States.RUNNING:
            # P ta saindo de READY e entrando em RUNNING
            self.time_stats.addTimeExitReady(time=instant_time)
            self.time_stats.addTimeEnterRunning(time=instant_time)

        elif new_state == States.EXIT:
            # saindo de RUNNING entrando em EXIT
            self.time_stats.addTimeExitRunning(time=instant_time)
            # definimos os tempos finais de cada estado e turnaround_time
            self.time_stats.defineFinalTimes()
            self.time_stats.setTurnaroundTime()

        # finalmente trocamos o status atual pro novo
        self.state = new_state

    def __str__(self):
        return f"PCB(pid={self.pid}, state={self.state}, source_file={self.source_file}, PC={self.pc}, acc={self.acc}, time_to_wait={self.time_to_wait})"