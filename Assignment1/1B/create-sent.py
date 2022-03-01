import sys

filename = sys.argv[1]

with open(filename,"r") as f:
	lines = f.readlines()
	lines = [line.split() for line in lines]

curstate = -1
sent = []
while(len(sent) == 0 or sent[-1] != "</s>"):
	if curstate == -1:
		for line in lines:
			if len(line) == 1:
				continue
			if line[2] == "<s>":
				curstate = line[1]
				break
	else:
		for line in lines:
			if len(line) == 1:
				continue
			if line[0] == curstate:
				curstate = line[1]
				sent.append(line[3])
				break
print(" ".join(sent[:-1]))