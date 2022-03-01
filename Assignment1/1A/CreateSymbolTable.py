import sys

vocabfile = sys.argv[1]

with open(vocabfile,"r") as f:
	lines = f.readlines()

g = open("SymbolTable.txt","w")
o = open("SymbolTableOutput.txt","w")
g.write("<eps>\t0\n")
o.write("<eps>\t0\n")
i = 1
for line in lines:
	line = line.strip('\n')
	word_list = [line]
	word_list = word_list + [str(i)+"\n"]
	g.write("\t".join(word_list))
	o.write("\t".join(word_list))
	i += 1
g.write(f"<s>\t{i}\n")
o.write(f"<s>\t{i}\n")
g.write(f"</s>\t{i+1}\n")
o.write(f"</s>\t{i+1}\n")
g.write(f"<unk>\t{i+2}\n")
o.write(f"<unk>\t{i+2}\n")
o.write(f"<blank>\t{i+3}\n")
g.close()
o.close()