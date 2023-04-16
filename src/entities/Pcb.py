from entities.enums.States import States
from entities.TimespentStats import TimespentStats
from parser.models.Program import Program
from parser.parser import Parser
from parser.models import Mnemonic


class PCB:
    state: States
    pid: int
    pc : Mnemonic
    acc: int
    source_file: str
    program: Program
    time_to_wait: int
    time_stats: TimespentStats

    def __init__(self, pid: int, source_file : str):
        self.pid = pid
        self.acc = 0
        self.source_file = source_file
        self.program = Parser(source_file).parse()
        self.pc = self.program.root
        self.time_stats = TimespentStats()
        self.state = None
        self.time_to_wait = 0

    def init_process(self, instant_time : int):
        self._init_state(States.READY, instant_time)
        self.time_to_wait = 0

    def block_process(self, instant_time : int, time_to_wait=8):
        self.time_to_wait = time_to_wait
        self._update_state(States.BLOCKED, instant_time)

    def unblock_process(self, instant_time : int, new_state=States.READY, ):
        self.time_to_wait = 0
        # Novo estado pode ser READY, ou outro; por isso pode receber por parametro
        self._update_state(new_state=new_state, instant_time=instant_time)
        # TODO: Ver o que mais vai acontecer quando um processo for desbloqueado

    def decrease_time_to_wait(self):
        self.time_to_wait -= 1

    def update(self, new_pc : Mnemonic, new_acc : int, instant_time : int, new_state = States.READY):
        self.pc = new_pc
        self.acc = new_acc
        self._update_state(new_state, instant_time)

    def _init_state(self, new_state : States, instant_time : int):
        if self.state is None:
            self.time_stats.add_time_enter_ready(time=instant_time)
            self.state = States.READY
        else:
            self._update_state(new_state, instant_time)

    def _update_state(self, new_state : States, instant_time : int):
        if new_state == self.state: # ja estou no novo state, nao precisa fazer nada
            pass
        elif new_state == States.BLOCKED:
            # P ta saindo de RUNNING e entrando em BLOCKED
            self.time_stats.add_time_exit_running(time=instant_time)
            self.time_stats.add_time_enter_blocked(time=instant_time)

        elif new_state == States.READY:
            # P ta saindo ou de BLOCKED ou de RUNNING e entrando em READY
            if self.state == States.BLOCKED:
                self.time_stats.add_time_exit_blocked(time=instant_time)
            elif self.state == States.RUNNING:
                self.time_stats.add_time_exit_running(time=instant_time)

            self.time_stats.add_time_enter_ready(time=instant_time)

        elif new_state == States.RUNNING:
            # P ta saindo de READY e entrando em RUNNING
            self.time_stats.add_time_exit_ready(time=instant_time)
            self.time_stats.add_time_enter_running(time=instant_time)

        elif new_state == States.EXIT:
            # saindo de RUNNING entrando em EXIT
            self.time_stats.add_time_exit_running(time=instant_time)
            # definimos os tempos finais de cada estado e turnaround_time
            self.time_stats.define_final_times()
            self.time_stats.set_turnaround_time()

        # finalmente trocamos o status atual pro novo
        self.state = new_state

    def is_ready(self):
        return self.state == States.READY

    def is_running(self):
        return self.state == States.RUNNING

    def is_exited(self):
        return self.state == States.EXIT

    def __str__(self):
        return f"pid={self.pid}, state={self.state}, source_file={self.source_file}, PC=({self.pc}), acc={self.acc}, time_to_wait={self.time_to_wait}, program=({self.program})"