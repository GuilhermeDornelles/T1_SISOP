from entities.InstructionData import InstructionData
from entities.enums.ReturnCode import ReturnCode

def next_step(instruction_data : InstructionData):
    instruction_data.pc = instruction_data.pc.next

def transform_value(instruction_data : InstructionData) -> str:
    value = instruction_data.pc.value
    if value[0] != '#' and instruction_data.data[value]:
        value = str(instruction_data.data[value])
    return value.replace('#', '')

def add(instruction_data : InstructionData):
    value = transform_value(instruction_data)
    instruction_data.acc = str(int(instruction_data.acc) + int(value))
    next_step(instruction_data)

def sub(instruction_data : InstructionData):
    value = transform_value(instruction_data)
    instruction_data.acc = str(int(instruction_data.acc) - int(value))
    next_step(instruction_data)

def mult(instruction_data : InstructionData):
    value = transform_value(instruction_data)
    instruction_data.acc = str(int(instruction_data.acc) * int(value))
    next_step(instruction_data)

def div(instruction_data : InstructionData):
    value = transform_value(instruction_data)
    instruction_data.acc = str(int(instruction_data.acc) // int(value))
    next_step(instruction_data)

def load(instruction_data : InstructionData): 
    instruction_data.acc = transform_value(instruction_data)
    next_step(instruction_data)

def store(instruction_data : InstructionData):
    value = instruction_data.pc.value
    instruction_data.data[value] = instruction_data.acc
    next_step(instruction_data)

def brany(instruction_data : InstructionData):
    value = instruction_data.pc.value
    instruction_data.pc = instruction_data.flags[value]

def brpos(instruction_data : InstructionData):
    value = instruction_data.pc.value
    if int(instruction_data.acc) > 0:
    	instruction_data.pc = instruction_data.flags[value]

def brzero(instruction_data : InstructionData):
    value = instruction_data.pc.value
    if int(instruction_data.acc) == 0:
    	instruction_data.pc = instruction_data.flags[value]

def brneg(instruction_data : InstructionData):
    value = instruction_data.pc.value
    if int(instruction_data.acc) < 0:
    	instruction_data.pc = instruction_data.flags[value]

def syscall(instruction_data : InstructionData):
    value = instruction_data.pc.value
    if value == "0":
        print("SYSCALL 0")
        return ReturnCode.EXIT
    elif value == "1":
        print("SYSCALL 1")
        print(f"ACC = {instruction_data.acc}")
        next_step(instruction_data)
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

        instruction_data.acc = new_acc
        next_step(instruction_data)
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
