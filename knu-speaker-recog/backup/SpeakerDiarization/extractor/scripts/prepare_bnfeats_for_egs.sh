#!/bin/bash

nj=30
cmd="run.pl"
stage=0
compress=true

echo "$0 $@"  # Print the command line for logging

if [ -f path.sh ]; then . ./path.sh; fi
. parse_options.sh || exit 1;

if [ $# != 3 ]; then
  echo "Usage: $0 <in-data-dir> <out-data-dir> <feat-dir>"
  echo "e.g.: $0 data/bnf data/bnf_nosil exp/bnf_nosil"
  echo "Options: "
  echo "  --nj <nj>                                        # number of parallel jobs"
  echo "  --cmd (utils/run.pl|utils/queue.pl <queue opts>) # how to run jobs."
  exit 1;
fi

data_in=$1
data_out=$2
dir=$3

name=`basename $data_in`

for f in $data_in/feats.scp $data_in/vad.scp $data_in/cmvn.scp ; do
  [ ! -f $f ] && echo "$0: No such file $f" && exit 1;
done

# Set various variables.
mkdir -p $dir/log
mkdir -p $data_out
featdir=$(utils/make_absolute.sh $dir)

cp $data_in/utt2spk $data_out/utt2spk
cp $data_in/spk2utt $data_out/spk2utt
cp $data_in/wav.scp $data_out/wav.scp
[ -f $data_in/segments ] && cp $data_in/segments $data_out/segments

write_num_frames_opt="--write-num-frames=ark,t:$featdir/log/utt2num_frames.JOB"

sdata_in=$data_in/split$nj;
utils/split_data.sh $data_in $nj || exit 1;

$cmd JOB=1:$nj $dir/log/create_bnfeats_${name}.JOB.log \
  apply-cmvn --norm-means=true --norm-vars=false --utt2spk=ark:${sdata_in}/JOB/utt2spk scp:${sdata_in}/JOB/cmvn.scp scp:${sdata_in}/JOB/feats.scp ark:- \| \
  select-voiced-frames ark:- scp,s,cs:${sdata_in}/JOB/vad.scp ark:- \| \
  copy-feats --compress=$compress $write_num_frames_opt ark:- \
  ark,scp:$featdir/bnfeats_${name}.JOB.ark,$featdir/bnfeats_${name}.JOB.scp || exit 1;

for n in $(seq $nj); do
  cat $featdir/bnfeats_${name}.$n.scp || exit 1;
done > ${data_out}/feats.scp || exit 1

for n in $(seq $nj); do
  cat $featdir/log/utt2num_frames.$n || exit 1;
done > $data_out/utt2num_frames || exit 1
rm $featdir/log/utt2num_frames.*

echo "$0: Succeeded creating bottleneck features with cvmn and vad for $name"
