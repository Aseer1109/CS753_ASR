import sys

def map_to_itself(vocab,w1,w2,w3,w4, iter):
	for i in range(len(vocab)):
		if(vocab[i] != w1 and vocab[i] != w2 and vocab[i] != w3 and vocab[i] != w4):
			f.write(str(iter) + "\t" + str(iter) + "\t" + vocab[i] + "\t" + vocab[i] + "\n")

def create_edge(iter, next_iter, w):
	f.write(str(iter) + "\t" + str(next_iter) + "\t" + w + "\t" + w + "\n")

w1 = sys.argv[1]
w2 = sys.argv[2]
w3 = sys.argv[3]
w4 = sys.argv[4]

vocab = []
with open("../1A/SymbolTable.txt","r") as f:
	for line in f.readlines():
		word, index = line.split()
		if word != "<eps>" and word != "<unk>":
			vocab.append(word)

f = open("T.txt","w")

# CREATING MAJOR IMPORTANT PATHS
create_edge(0, 1, w1)
create_edge(3, 4, w1)
create_edge(9, 10, w1)
create_edge(6, 7, w1)
create_edge(12, 13, w1)

create_edge(1, 2, w2)
create_edge(4, 5, w2)
create_edge(10, 11, w2)
create_edge(7, 8, w2)
create_edge(13, 14, w2)

create_edge(0, 3, w3)
create_edge(1, 4, w3)
create_edge(2, 5, w3)
create_edge(6, 12, w3)
create_edge(7, 13, w3)
create_edge(8, 14, w3)

create_edge(3, 9, w4)
create_edge(4, 10, w4)
create_edge(5, 11, w4)
create_edge(0, 6, w4)
create_edge(1, 7, w4)
create_edge(2, 8, w4)

create_edge(0, 15, w2)
create_edge(3, 15, w2)
create_edge(9, 15, w2)
create_edge(6, 15, w2)
create_edge(12, 15, w2)

for i in range(16):
	map_to_itself(vocab,w1,w2,w3,w4,i)

f.write("11\n14\n")
f.close()