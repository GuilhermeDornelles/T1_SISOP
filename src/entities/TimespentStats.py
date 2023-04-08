
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
    
    def setTurnaroundTime(self):
        # pega o primeiro instante que foi pra READY
        primeiro_ready, bla = self.time_ready[0]
        # o ultimo instante que saiu de RUNNING (instante que acabou de rodar a ultima instrucao)
        bla, ultimo_running = self.time_running[-1]
        self.turnaround_time = ultimo_running - primeiro_ready

    # addTimeEnter vai adicionar uma tupla (tempo_que_entrou , None) no fim da lista
    # addTimeExit vai substituir o None da ultima posicao da lista (que vai estar (tempo_que_entrou, None)) pelo tempo que saiu do estado

    def addTimeEnterRunning(self, time : int):
        self.time_running.append((time, None))

    def addTimeExitRunning(self, time : int):
        enter, bla = self.time_running[-1]
        self.time_running[-1] = (enter, time)

    def addTimeEnterReady(self, time : int):
        self.time_ready.append((time, None))

    def addTimeExitReady(self, time : int):
        enter, bla = self.time_ready[-1]
        self.time_ready[-1] = (enter, time)
    
    def addTimeEnterBlocked(self, time : int):
        self.time_blocked.append((time, None))

    def addTimeExitBlocked(self, time : int):
        enter, bla = self.time_blocked[-1]
        self.time_blocked[-1] = (enter, time)

    def defineFinalTimes(self):
        self.final_time_ready = self.auxCalculusFinalTime(field=self.time_ready)
        self.final_time_running = self.auxCalculusFinalTime(field=self.time_running)
        self.final_time_blocked = self.auxCalculusFinalTime(field=self.time_blocked)

    def auxCalculusFinalTime(self, field : list[tuple[int, int]]) -> int:
        soma = 0
        for item in field:
            enter_time, exit_time = item
            soma += (exit_time - enter_time)
        return soma
