python part_A.py $@
/opt/kaldi/tools/openfst/bin/fstcompile --isymbols=SymbolTableOutput.txt --osymbols=SymbolTable.txt F.txt F.fst
/opt/kaldi/tools/openfst/bin/fstcompose F.fst L.fst FoL.fst
/opt/kaldi/tools/openfst/bin/fstshortestpath FoL.fst short.fst
/opt/kaldi/tools/openfst/bin/fstprint --isymbols=SymbolTableOutput.txt --osymbols=SymbolTable.txt short.fst short.txt
python fill.py short.txt