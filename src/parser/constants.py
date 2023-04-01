
def add(coisa, value):
    coisa.acc += value

def sub(coisa, value):
    coisa.acc -= value

def mult(coisa, value):
    coisa.acc *= value
    
def div(coisa, value):
    coisa.acc /= value

def load(coisa, value):
    coisa.acc = value

def store(coisa, value):
    coisa.data[value] = coisa.acc
    
def brany(coisa, value):
    coisa.pc = coisa.flags[value]
    
def brpos(coisa, value):
    if coisa.acc > 0:
    	coisa.pc = coisa.flags[value]

def brzero(coisa, value):
    if coisa.acc == 0:
    	coisa.pc = coisa.flags[value]
        
def brneg(coisa, value):
    if coisa.acc < 0:
    	coisa.pc = coisa.flags[value]
        
def syscall(coisa, value):
	if value == '0':
        # chama funcao para terminar execucao do processo
        # vai mandar ele pra lista de 'finalizados' e/ou trocar o status na PCB
		coisa.faz_isso()
	if value == '1':
        # chama funcao que vai printar na tela
        # vai printar acc na tela e depois mandar o processo pra lista de bloqueados, deixando ele lá por 8/9/10 unidades de tempo
		coisa.faz_isso1()
	if value == '2':
        # chama a funcao que vai pedir leitura do teclado
        # vai pedir que o usuario insira qualquer valor inteiro via teclado, (duvida se nesse caso esse valor é salvo no acc? ou o que)
        # e depois mandar P pra lista de bloqueados, deixando ele lá por 8/9/10 unidades de tempo 
		coisa.faz_isso2()

constants = {
    'ADD': add,
    'SUB': sub,
    'MULT': mult,
    'DIV': div,
    'LOAD': load,
    'STORE': store,
    'BRANY': brany,
    'BRPOS': brpos,
    'BRZERO': brzero,
    'BRNEG': brneg,
    'SYSCALL': syscall,
}
