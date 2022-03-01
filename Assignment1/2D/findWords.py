import os
from random import sample
import sys, subprocess

inpwords = sys.argv[2:]

trainTextFile = "data/train/text"

data = {}

with open(trainTextFile, "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()

		speaker = line[0][:6]

		textid = line[0]

		words = line[1:]

		for word in words:
			if speaker in data:
				data[speaker].append((word, textid))
			else:
				data[speaker] = [(word, textid)]

for speaker in data:
	found = True
	utts = []
	for word in inpwords:
		if word not in dict(data[speaker]):
			found = False
			break
		else:
			utts.append((word, dict(data[speaker])[word]))
	
	if not found:
		continue

	if found:
		break

lexiconfile = "lang/phones/align_lexicon.txt"
lexicon = {}

with open(lexiconfile, "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()

		word = line[0]

		lexicon[word] = line[2:]

		assert(line[0] == line[1])

uttphones = []

phonefile = "lang/phones.txt"
phone2Id = {}

with open(phonefile, "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()

		phone = line[0]

		phone2Id[phone] = line[1]

wavscpfile = "data/train/wav.scp"
wavefilemap = {}

with open(wavscpfile, "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()

		wavefilemap[line[0]] = line[1]

alignmentfile = sys.argv[1]
uttAlign = {}

with open(alignmentfile, "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()

		uttid = line[0]
		uttstart = line[2]
		uttend = line[3]
		phoneid = line[4]

		if uttid in uttAlign:
			uttAlign[uttid][phoneid] = (uttstart, uttend)
		else:
			uttAlign[uttid] = {phoneid: (uttstart, uttend)}

for word, uttid in utts:
	phones = lexicon[word]
	uttword = []
	for phone in phones:
		uttword.append((phone2Id[phone], uttid, uttAlign[uttid][phone2Id[phone]]))
	uttphones.append(uttword)

if not os.path.exists("soxtemp"):
	os.mkdir("soxtemp")

sampleRate = subprocess.run(["soxi", "-r", wavefilemap[utts[0][1]]], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

# Generate studio silence with sox
subprocess.run(["sox", "-n", "-r", sampleRate, os.path.join("soxtemp", "silence.wav"), "trim", "0.0", "0.2"])

idx = 0
for uttword in uttphones:
	for phone, uttid, (uttstart, uttend) in uttword:
		subprocess.run(["sox", wavefilemap[uttid], os.path.join("soxtemp", "trimmed" + str(idx) + ".wav"), "trim", uttstart, uttend])
		idx += 1

trimfiles = []
idx = 0
for idx1, uttword in enumerate(uttphones):
	for phone, uttid, (uttstart, uttend) in uttword:
		trimfiles.append(os.path.join("soxtemp", "trimmed" + str(idx) + ".wav"))
		idx += 1

	if idx1 != len(uttphones) - 1:
		trimfiles.append(os.path.join("soxtemp", "silence.wav"))

subprocess.run(["sox"] + trimfiles + ["out.wav"])
