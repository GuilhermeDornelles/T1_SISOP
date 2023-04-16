from entities.Context import Context
from entities.enums.ReturnCode import ReturnCode

def next_step(context : Context):
    context.pc = context.pc.next

def transform_value(context : Context) -> str:
    value = context.pc.value
    if value[0] != '#' and context.data[value]:
        value = str(context.data[value])
    return value.replace('#', '')

def add(context : Context):
    value = transform_value(context)
    context.acc = str(int(context.acc) + int(value))
    next_step(context)

def sub(context : Context):
    value = transform_value(context)
    context.acc = str(int(context.acc) - int(value))
    next_step(context)

def mult(context : Context):
    value = transform_value(context)
    context.acc = str(int(context.acc) * int(value))
    next_step(context)

def div(context : Context):
    value = transform_value(context)
    context.acc = str(int(context.acc) // int(value))
    next_step(context)

def load(context : Context): 
    context.acc = transform_value(context)
    next_step(context)

def store(context : Context):
    value = context.pc.value
    context.data[value] = context.acc
    next_step(context)

def brany(context : Context):
    value = context.pc.value
    context.pc = context.flags[value]

def brpos(context : Context):
    value = context.pc.value
    if int(context.acc) > 0:
    	context.pc = context.flags[value]

def brzero(context : Context):
    value = context.pc.value
    if int(context.acc) == 0:
    	context.pc = context.flags[value]

def brneg(context : Context):
    value = context.pc.value
    if int(context.acc) < 0:
    	context.pc = context.flags[value]

def syscall(context : Context):
    value = context.pc.value
    if value == "0":
        print("SYSCALL 0")
        return ReturnCode.EXIT
    elif value == "1":
        print("SYSCALL 1")
        print(f"ACC = {context.acc}")
        next_step(context)
        return ReturnCode.OUTPUT
    elif value == "2":
        print("SYSCALL 2")
        valid_value = False
        new_acc = 0
        while not valid_value:
            try:
                input_raw = input("Insira o novo valor para o acumulador (numero inteiro): ")
                new_acc = int(input_raw)
                valid_value = True
            except ValueError:
                print("Valor inserido invalido. Tente novamente.")
                valid_value = False

        context.acc = new_acc
        next_step(context)
        return ReturnCode.INPUT

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
