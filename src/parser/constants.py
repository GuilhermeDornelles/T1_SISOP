
def nextStep(program):
    program.pc = program.pc.next

def add(program, value):
    program.acc += value
    nextStep(program)

def sub(program, value):
    program.acc -= value
    nextStep(program)

def mult(program, value):
    program.acc *= value
    nextStep(program)
    
def div(program, value):
    program.acc /= value
    nextStep(program)

def load(program, value):
    program.acc = value
    nextStep(program)

def store(program, value):
    program.data[value] = program.acc
    nextStep(program)
    
def brany(program, value):
    program.pc = program.flags[value]
    
def brpos(program, value):
    if program.acc > 0:
    	program.pc = program.flags[value]

def brzero(program, value):
    if program.acc == 0:
    	program.pc = program.flags[value]
        
def brneg(program, value):
    if program.acc < 0:
    	program.pc = program.flags[value]
        
#TODO: como passar comando de volta pra PCB pra encerrar ou esperar       
def syscall(program, value):
    if value == '0':
        # chama funcao para terminar execucao do processo
        # vai mandar ele pra lista de 'finalizados' e/ou trocar o status na PCB
        nextStep(program)
    if value == '1':
        # chama funcao que vai printar na tela
        # vai printar acc na tela e depois mandar o processo pra lista de bloqueados, deixando ele lá por 8/9/10 unidades de tempo
        nextStep(program)
    if value == '2':
        # chama a funcao que vai pedir leitura do teclado
        # vai pedir que o usuario insira qualquer valor inteiro via teclado, (duvida se nesse caso esse valor é salvo no acc? ou o que)
        # e depois mandar P pra lista de bloqueados, deixando ele lá por 8/9/10 unidades de tempo 
        nextStep(program)


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
