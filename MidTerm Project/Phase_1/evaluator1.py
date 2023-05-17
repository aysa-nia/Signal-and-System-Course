import os
from scipy.io import wavfile as wav
from Levenshtein import distance as levenshtein_distance

from DTMF1 import DTMF

sound_path = 'single-digit-dataset'
sound_files = os.listdir(sound_path)
correct_file = 'label.csv'
start_idx = 0
correct_f = open(correct_file)
correct = correct_f.readlines()[1:]
for i in range(len(correct)):
        if correct[i]!=correct[-1]:
                correct[i] = correct[i][:-1]
        correct[i] = correct[i].split(',')
        correct[i][0] = int(correct[i][0])
correct_f.close()
loss = 0
all_point = 0
for sound_file in sound_files:
        rate, data = wav.read(os.path.join(sound_path, sound_file))
        result = str("'")+DTMF(data, rate)+str("'")
        (file, ext) = os.path.splitext(sound_file)
        file = int(file)
        correct_result = correct[file-start_idx][1].strip('\n')
        loss += levenshtein_distance(result, correct_result)
print('your loss is:',loss/len(correct))

