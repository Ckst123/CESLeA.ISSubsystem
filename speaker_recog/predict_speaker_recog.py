"""
this code uses Python's hmmlearn library to implement HMM.
"""
import numpy as np
import os
from speaker_recog.wav2features import wav2mfcc
from sklearn.externals import joblib

np.set_printoptions(threshold=25000)


"""
https://stackoverflow.com/questions/14463277/how-to-disable-python-warnings
"""
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


target_fs = 16000
winlen = 0.025
winstep = 0.01
nfilt = 29
numcep = 13

speaker_names = ['den','ami','jan','jun','lee','lim','moh','nas','pro','son','woo','you', 'kst', 'kms', 'lsw']

hmmfile = 'hmm_spr.pkl'

if os.path.exists(hmmfile):
    hmms = joblib.load("hmm_spr.pkl")
else:
    print('no pickle file')
    exit(1)


def sample_process(sample, temp_len):
    temp_len_new = []
    A = sample
    print('len',len(sample))
    for i in range(1):
        temp_len_new = np.append(len(sample[i]), (len(sample[i + 1]), len(sample[i + 2]), len(sample[i + 3]), len(sample[i + 4]), len(sample[i + 5]), len(sample[i + 6])))

    data = np.concatenate([A[i] for i in range(len(sample))])

    temp_len_new = np.array(temp_len_new, dtype=int)
    return temp_len_new, data, A


def predict(name):
    mcep, fs, x = wav2mfcc(name, target_fs, winlen, winstep, nfilt, numcep)
    pout = []
    for k in range(len(hmms)):
        po = hmms[k].score(mcep)
        pout.append(po)
    max_value = max(pout)
    max_index = pout.index(max_value)
    max_name = speaker_names[max_index]
    return max_index, max_name


if __name__ == "__main__":
    for folder in os.listdir('test'):
        for names in os.listdir('test/%s'%folder):
            fname = os.path.join('test', folder, names)
            print(fname, predict(fname))