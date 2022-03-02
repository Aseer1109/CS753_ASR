import random

with open("/opt/kaldi/egs/wolof/data/dev/wav.scp", "r") as f:
	lines = [line.split() for line in f.readlines()]

devutts = random.sample(lines, random.randint(1, len(lines)))
devtext = []

with open("/opt/kaldi/egs/wolof/data/dev/text", "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()
	
		if line[0] in dict(devutts):
			devtext.append(" ".join(line))

with open("/opt/kaldi/egs/wolof/data/test/wav.scp", "r") as f:
	lines = [line.split() for line in f.readlines()]

testutts = random.sample(lines, random.randint(1, len(lines)))
testtext = []

with open("/opt/kaldi/egs/wolof/data/test/text", "r") as f:
	lines = f.readlines()

	for line in lines:
		line = line.split()
	
		if line[0] in dict(testutts):
			testtext.append(" ".join(line))

utts = sorted(devutts + testutts)
text = sorted(devtext + testtext)
utt2spk = []

for utt in utts:
	utt2spk.append((utt[0], utt[0][:6]))

with open("/opt/kaldi/egs/wolof/data/truetest/wav.scp", "w") as f:
	for utt in utts:
		f.write(utt[0] + "\t" + utt[1] + "\n")

with open("/opt/kaldi/egs/wolof/data/truetest/text", "w") as f:
	for line in text:
		f.write(line + "\n")

with open("/opt/kaldi/egs/wolof/data/truetest/utt2spk", "w") as f:
	for utt in utt2spk:
		f.write(utt[0] + "\t" + utt[1] + "\n")