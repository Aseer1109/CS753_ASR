python part_B.py $@
/opt/kaldi/tools/openfst/bin/fstcompile --isymbols=../1A/SymbolTable.txt --osymbols=../1A/SymbolTable.txt T.txt T.fst
/opt/kaldi/tools/openfst/bin/fstcompose T.fst ../1A/L.fst ToL.fst
/opt/kaldi/tools/openfst/bin/fstshortestpath ToL.fst short.fst
/opt/kaldi/tools/openfst/bin/fstprint --isymbols=../1A/SymbolTable.txt --osymbols=../1A/SymbolTable.txt short.fst short.txt
python create-sent.py short.txt