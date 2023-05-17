from scipy.io import wavfile as wav
from DTMF1 import DTMF
import numpy as np
import os


def save_as_csv(results):
    with open("Results1.csv", "w") as resFile:
        resFile.write("Id,Expected\n")
        for sample in results:
            resFile.write("{},'{}'\n".format(sample[0], "".join(sample[1])))

results = []
for sample in os.listdir('single-digit-dataset'):
    rate, data = wav.read('single-digit-dataset\\'+sample)
    sample = sample.split('.')[0]
    if len(data.T.shape) > 1:
        data = data.T[0]  # Extracting the main channel of the sound
    result = DTMF(data, rate)
    results.append((sample, result))


save_as_csv(results)
