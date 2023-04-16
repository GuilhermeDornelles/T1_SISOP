# Print usado para coisas IMPORTANTES, informações que o sor pediu que tivesse nos logs
# TODO sor pediu que seria bom se criassemos uma forma de enviar os prints (logs) pra algum arquivo p ficar salvo
def super_print(string : str):
    init_mark = '#' * (len(string) + 6)
    print(init_mark)
    lines = string.split("\n")
    for line in lines:
        print(f"## {line} ##")
    print(init_mark)