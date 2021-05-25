import contextlib
import wave
import os
import random
import numpy as np
import librosa
from llsollu.requests_fn import asr
from googletest import google_stt


def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (16000, )
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_wave(path, audio):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio)


if __name__ == '__main__':
    b1 = read_wave('test1.wav')[0]
    b2 = read_wave('test3.wav')[0]

    D = np.frombuffer(b1, dtype=np.int16)
    data = librosa.core.resample(1.0 * D, orig_sr=16000, target_sr=8000).astype(dtype=np.int16).tobytes()
    llsollu_ans1 = asr(data)
    D = np.frombuffer(b2, dtype=np.int16)
    data = librosa.core.resample(1.0 * D, orig_sr=16000, target_sr=8000).astype(dtype=np.int16).tobytes()
    llsollu_ans2 = asr(data)

    ans1 = google_stt('testo1.wav')
    ans3 = google_stt('testo2.wav')

    b1 = read_wave('testo1.wav')[0]
    b2 = read_wave('testo2.wav')[0]

    D = np.frombuffer(b1, dtype=np.int16)
    data = librosa.core.resample(1.0 * D, orig_sr=16000, target_sr=8000).astype(dtype=np.int16).tobytes()
    llsollu_ans1o = asr(data)

    D = np.frombuffer(b2, dtype=np.int16)
    data = librosa.core.resample(1.0 * D, orig_sr=16000, target_sr=8000).astype(dtype=np.int16).tobytes()
    llsollu_ans2o = asr(data)

    print(llsollu_ans1o)
    print(llsollu_ans1)
    print(ans1)

    print(llsollu_ans2o)
    print(llsollu_ans2)
    print(ans3)

    b1 = read_wave('testo1.wav')[0]
    b2 = read_wave('testo2.wav')[0]
    b3 = read_wave('testo3.wav')[0]

    D1 = np.frombuffer(b1, dtype=np.int16)
    D2 = np.frombuffer(b2, dtype=np.int16)
    D3 = np.frombuffer(b3, dtype=np.int16)

    D = ( 1.0 * D1 + 1.0 * D2 + 1.0 * D3) / 3.0
    bo = D.astype(np.int16).tobytes()
    write_wave('testo.wav', bo)

    ans = google_stt('testo.wav')

    print(ans)
