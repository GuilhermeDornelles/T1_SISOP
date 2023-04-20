# Print usado para coisas IMPORTANTES, informações que o sor pediu que tivesse nos logs
def super_print(string : str):
    init_mark = '#' * (len(string) + 6)
    print(init_mark)
    lines = string.split("\n")
    for line in lines:
        print(f"## {line} ##")
    # print(init_mark)