import sys

n = len(sys.argv)
sentence = sys.argv[1:n]
sentence = ["<s>"]+sentence+["<\s>"]

vocab = []
with open("SymbolTable.txt","r") as f:
	for line in f.readlines():
		word, index = line.split()
		if word != "<eps>" and word != "<s>" and word != "</s>" and word != "<unk>":
			vocab.append(word)

f = open("F.txt","w")
for i in range(len(sentence)-1):
	if(sentence[i] != "XXX"):
		f.write(str(i) + "\t" + str(i+1) + "\t" + sentence[i] + "\t" + sentence[i] + "\n")
	else:
		for j in vocab:
			f.write(str(i) + "\t" + str(i+1) + "\t" + "<blank>" + "\t" + j + "\t\n")

f.write(str(n)+"\t"+str(n+1)+"\t"+"</s>"+"\t"+"</s>"+"\n")

f.write(str(n+1))
f.close()