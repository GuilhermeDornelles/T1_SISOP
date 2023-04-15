
class TimespentStats:
    # os tempos vao ser armazenados assim:
    # [(a, b), (a, b), (a, b)]
    # sendo 'a' o momento que foi para X estado e 'b' o momento que saiu de X estado
    # o tempo total em X estado vai ser calculado pela soma das diferenças de cada (a, b)

    time_ready : list[tuple[int, int]]
    time_running : list[tuple[int, int]]
    time_blocked : list[tuple[int, int]]
    final_time_ready : int
    final_time_running : int
    final_time_blocked : int

    turnaround_time : int

    def __init__(self):
        self.time_ready = []
        self.time_running = []
        self.time_blocked = []
    
    def set_turnaround_time(self):
        # pega o primeiro instante que foi pra READY
        primeiro_ready, bla = self.time_ready[0]
        # o ultimo instante que saiu de RUNNING (instante que acabou de rodar a ultima instrucao)
        bla, ultimo_running = self.time_running[-1]
        self.turnaround_time = ultimo_running - primeiro_ready

    # addTimeEnter vai adicionar uma tupla (tempo_que_entrou , None) no fim da lista
    # addTimeExit vai substituir o None da ultima posicao da lista (que vai estar (tempo_que_entrou, None)) pelo tempo que saiu do estado

    def add_time_enter_running(self, time : int):
        self.time_running.append((time, None))

    def add_time_exit_running(self, time : int):
        print(f"t r {self.time_running}")
        enter, bla = self.time_running[-1]
        self.time_running[-1] = (enter, time)

    def add_time_enter_ready(self, time : int):
        self.time_ready.append((time, None))

    def add_time_exit_ready(self, time : int):
        enter, bla = self.time_ready[-1]
        self.time_ready[-1] = (enter, time)
    
    def add_time_enter_blocked(self, time : int):
        self.time_blocked.append((time, None))

    def add_time_exit_blocked(self, time : int):
        enter, bla = self.time_blocked[-1]
        self.time_blocked[-1] = (enter, time)

    def define_final_times(self):
        self.final_time_ready = self._auxCalculusFinalTime(field=self.time_ready)
        self.final_time_running = self._auxCalculusFinalTime(field=self.time_running)
        self.final_time_blocked = self._auxCalculusFinalTime(field=self.time_blocked)

    def _auxCalculusFinalTime(self, field : list[tuple[int, int]]) -> int:
        soma = 0
        for item in field:
            enter_time, exit_time = item
            soma += (exit_time - enter_time)
        return soma

    def final_times(self) -> str:
        self.define_final_times()
        return f"final_time_ready={self.final_time_ready}, final_time_blocked={self.final_time_blocked}, final_time_running={self.final_time_running}"