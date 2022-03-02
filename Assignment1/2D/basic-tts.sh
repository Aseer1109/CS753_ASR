dir="exp/tri1_dat_aug/"

for i in  $dir/ali.*.gz;
do ../../src/bin/ali-to-phones --ctm-output $dir/final.mdl ark:"gunzip -c $i|" -> ${i%.gz}.ctm;
done;

cat $dir/*.ctm > $dir/merged_alignment.txt

python $(dirname $0)/findWords.py $dir/merged_alignment.txt $@
