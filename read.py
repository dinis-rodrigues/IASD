


f = open('example.txt', 'r') 
for line in f: 
	if line == '\n':
		pass
	print(type(line) )