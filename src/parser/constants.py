def next_step(scheduler):
    scheduler.pc = scheduler.pc.next

def add(scheduler, value):
    scheduler.acc += value
    next_step(scheduler)

def sub(scheduler, value):
    scheduler.acc -= value
    next_step(scheduler)

def mult(scheduler, value):
    scheduler.acc *= value
    next_step(scheduler)

def div(scheduler, value):
    scheduler.acc /= value
    next_step(scheduler)

def load(scheduler, value):
    scheduler.acc = value
    next_step(scheduler)

def store(scheduler, value):
    scheduler.data[value] = scheduler.acc
    next_step(scheduler)

def brany(scheduler, value):
    scheduler.pc = scheduler.flags[value]

def brpos(scheduler, value):
    if scheduler.acc > 0:
    	scheduler.pc = scheduler.flags[value]

def brzero(scheduler, value):
    if scheduler.acc == 0:
    	scheduler.pc = scheduler.flags[value]

def brneg(scheduler, value):
    if scheduler.acc < 0:
    	scheduler.pc = scheduler.flags[value]

def syscall(scheduler, value):
    scheduler.syscall(value)
    next_step(scheduler)

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
