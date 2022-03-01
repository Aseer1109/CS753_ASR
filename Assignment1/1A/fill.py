import sys

filename = sys.argv[1]

with open(filename,"r") as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()

		if "<blank>" in line:
			ans = line[3]
			print(line[3])
			exit()