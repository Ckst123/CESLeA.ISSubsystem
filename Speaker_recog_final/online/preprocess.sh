#!/bin/bash
# Copyright   2017   Johns Hopkins University (Author: Daniel Garcia-Romero)
#             2017   Johns Hopkins University (Author: Daniel Povey)
#        2017-2018   David Snyder
#             2018   Ewald Enzinger
#             2019   Yi Liu. Modified to support network training using TensorFlow
#             2019   Minsoo Kim
# Apache 2.0.
#
# See ../README.txt for more info on data required.

. ./cmd.sh
. ./path.sh
set -e

# The kaldi voxceleb egs dir
kaldi_voxceleb=$KALDI_ROOT/egs/voxceleb
data=$PROJECT_ROOT/data
exp=$PROJECT_ROOT/preprocess_log
mfccdir=$PROJECT_ROOT/mfcc
vaddir=$PROJECT_ROOT/mfcc
datadir=$DATA_ROOT
nnetdir=$PROJECT_ROOT/basemodel/xvector_nnet_pretrain

if [ $# != 1 ]; then
  echo "Usage: $0 <stage>"
  echo "e.g.: $0 train"
  echo "e.g.: $0 test"
  exit 1;
fi

stage=$1

if [ $stage = train ]; then
  rm -rf $data/spkrs
  make_data_all.pl $datadir/train $data/spkrs
  # Make MFCCs and compute the energy-based VAD for each dataset
  for name in spkrs; do
    steps/make_mfcc.sh --write-utt2num-frames true \
      --mfcc-config conf/mfcc.conf --nj 1 --cmd "$train_cmd" \
      $data/${name} $exp/make_mfcc $mfccdir
    utils/fix_data_dir.sh $data/${name}
    sid/compute_vad_decision.sh --nj 1 --cmd "$train_cmd" \
      $data/${name} $exp/make_vad $vaddir
    utils/fix_data_dir.sh $data/${name}
    cp $data/${name}/vad.scp $data/${name}/split1/1/vad.scp
  done
fi

if [ $stage = test ]; then
  rm -rf $data/test/* $nnetdir/xvectors_test/xvector*
  cp trials $data/test/trials
  make_data_test.pl $datadir $data/test
  # Make MFCCs and compute the energy-based VAD for each dataset
  for name in test; do
    make_mfcc_online.sh --write-utt2num-frames true \
      --mfcc-config conf/mfcc.conf --nj 1 --cmd "$train_cmd" \
      $data/${name} $exp/make_mfcc $mfccdir
    #utils/fix_data_dir.sh $data/${name}
    sid/compute_vad_decision.sh --nj 1 --cmd "$train_cmd" \
      $data/${name} $exp/make_vad $vaddir
    #utils/fix_data_dir.sh $data/${name}
    cp $data/${name}/vad.scp $data/${name}/split1/1/vad.scp
  done
fi
if [ $stage = test_offline ]; then
  rm -rf $data/test_offline
  make_data_test_offline.pl $datadir $data/test
  # Make MFCCs and compute the energy-based VAD for each dataset
  for name in test; do
    steps/make_mfcc.sh --write-utt2num-frames true \
      --mfcc-config conf/mfcc.conf --nj 1 --cmd "$train_cmd" \
      $data/${name} $exp/make_mfcc $mfccdir
    utils/fix_data_dir.sh $data/${name}
    sid/compute_vad_decision.sh --nj 1 --cmd "$train_cmd" \
      $data/${name} $exp/make_vad $vaddir
    utils/fix_data_dir.sh $data/${name}
    cp $data/${name}/vad.scp $data/${name}/split1/1/vad.scp
  done
fi
