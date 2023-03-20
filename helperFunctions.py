import librosa
import numpy as np
from pydub import AudioSegment

def extract_mfcc(filename):
    y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y).T, axis=0)
    rms = np.mean(librosa.feature.rms(y=y).T, axis=0)

    mfcc = np.array([mfcc])
    zcr = np.array([zcr])
    rms = np.array([rms])

    mfcc = np.expand_dims(mfcc, -1)
    zcr = np.expand_dims(zcr, -1)
    rms = np.expand_dims(rms, -1)

    res = np.hstack((rms, zcr, mfcc))

    return res

def print_output(output_arr):
# Categories = ['negative', 'neutral', 'positive']
    if (np.argmax(output_arr[0]) == 0): return 'Negative'
    if (np.argmax(output_arr[0]) == 1): return 'Neutral'
    if (np.argmax(output_arr[0]) == 2): return 'Positive'