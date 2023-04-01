
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
		coisa.faz_isso()
	if value == '1':
		coisa.faz_isso1()
	if value == '2':
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
