from parser.parser import Parser

parser = Parser('./src/tests/prog1.txt')

parser.parse()

current = parser.alguma_coisa.root

while current.next is not None:
	print(current)
	current = current.next
