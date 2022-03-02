#!/bin/bash

# This script trains + decodes a baseline ASR system for Wolof.

# initialization PATH
. ./path.sh  || die "path.sh expected";
# initialization commands
. ./cmd.sh

[ ! -L "steps" ] && ln -s ../wsj/s5/steps

[ ! -L "utils" ] && ln -s ../wsj/s5/utils

###############################################################
#                   Configuring the ASR pipeline
###############################################################
stage=0    # from which stage should this script start
nj=12        # number of parallel jobs to run during training
test_nj=2    # number of parallel jobs to run during decoding
# the above two parameters are bounded by the number of speakers in each set
###############################################################


# Stage 1: Prepares the train/dev data. Prepares the dictionary and the
# language model.
if [ $stage -le 1 ]; then
  > lang/dict/silence_phones.txt
  echo "Preparing lexicon and language models"
  local/prepare_lexicon.sh
  local/prepare_lm.sh
fi

# Feature extraction
# Stage 2: MFCC feature extraction + mean-variance normalization
if [ $stage -le 2 ]; then
   
   for x in train dev test; do
      steps/make_mfcc.sh --nj 8 --cmd "$train_cmd" data/$x exp/make_mfcc/$x mfcc
      steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc
   done
fi

# Stage 3: Training and decoding monophone acoustic models
if [ $stage -le 3 ]; then
  ### Monophone
    echo "Monophone training"
	  steps/train_mono.sh --nj "$nj" --cmd "$train_cmd" data/train lang exp/mono
    echo "Monophone training done"
    (
    echo "Decoding the test and dev set (Monophone)"
    utils/mkgraph.sh lang exp/mono exp/mono/graph

  
    # This decode command will need to be modified when you 
    # want to use tied-state triphone models 
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/mono/graph data/test exp/mono/decode_test
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/mono/graph data/dev exp/mono/decode_dev
    echo "Monophone decoding done."
    ) &
fi
wait;

# Stage 4: Training tied-state triphone acoustic models
if [ $stage -le 4 ]; then
  ### Triphone
    echo "Triphone training"
    steps/align_si.sh --nj $nj --cmd "$train_cmd" \
       data/train lang exp/mono exp/mono_ali
	  steps/train_deltas.sh --boost-silence 1.25  --cmd "$train_cmd"  \
	     2500 25000 data/train lang exp/mono_ali exp/tri1
    echo "Triphone training done"
	  #Add triphone decoding steps here #
    (
    echo "Decoding the test and dev set (Triphone)"
    utils/mkgraph.sh lang exp/tri1 exp/tri1/graph
  
    # This decode command will need to be modified when you 
    # want to use tied-state triphone models 
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/tri1/graph data/test exp/tri1/decode_test
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/tri1/graph data/dev exp/tri1/decode_dev
    echo "Triphone decoding done."
    ) &

fi
wait;

# # Stage 5
if [ $stage -le 5 ]; then
    echo "Data Augmentation"  
    utils/data/perturb_data_dir_speed_3way.sh data/train data/train_sp3

    for x in train_sp3; do
       steps/make_mfcc.sh --nj 8 --cmd "$train_cmd" data/$x exp/make_mfcc/$x mfcc
       steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc
    done

    ### Monophone
    echo "Monophone training (augmented)"
	  steps/train_mono.sh --nj "$nj" --cmd "$train_cmd" data/train_sp3 lang exp/mono_dat_aug
    echo "Monophone training done (augmented)"

    (
    echo "Decoding the test set (Monophone augmented)"
    utils/mkgraph.sh lang exp/mono_dat_aug exp/mono_dat_aug/graph

  
    # This decode command will need to be modified when you 
    # want to use tied-state triphone models 
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/mono_dat_aug/graph data/test exp/mono_dat_aug/decode_test
    echo "Monophone decoding done (augmented)"
    ) &
    wait;
        
    ### Triphone
    echo "Triphone training (augmented)"
    steps/align_si.sh --nj $nj --cmd "$train_cmd" \
       data/train_sp3 lang exp/mono_dat_aug exp/mono_ali_dat_aug
    steps/train_deltas.sh --boost-silence 1.25  --cmd "$train_cmd"  \
	     2500 25000 data/train_sp3 lang exp/mono_ali_dat_aug exp/tri1_dat_aug
	     
    echo "Triphone training done (augmented)"
    (
    echo "Decoding the test and dev set (triphone augmented)"
    utils/mkgraph.sh lang exp/tri1_dat_aug exp/tri1_dat_aug/graph
  
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/tri1_dat_aug/graph data/test exp/tri1_dat_aug/decode_test
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/tri1_dat_aug/graph data/dev exp/tri1_dat_aug/decode_dev
    echo "Triphone decoding done (augmented)"
    ) &
fi
wait;

# # Stage 6
if [ $stage -le 6 ]; then

    for x in truetest; do
       steps/make_mfcc.sh --nj 8 --cmd "$train_cmd" data/$x exp/make_mfcc/$x mfcc
       steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc
    done

    (
    echo "Decoding on the true test set"
    utils/mkgraph.sh lang exp/tri1_dat_aug exp/tri1_dat_aug/graph
  
    steps/decode.sh --nj $test_nj --cmd "$decode_cmd" \
      exp/tri1_dat_aug/graph data/truetest exp/tri1_dat_aug/decode_truetest
    echo "Triphone decoding done on true test set"
    ) &
fi

wait;
#score
# Computing the best WERs
for x in exp/*/decode*; do [ -d $x ] && grep WER $x/wer_* | utils/best_wer.sh; done
