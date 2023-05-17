import scipy
from scipy.io import wavfile as wav
import numpy as np
import math
from matplotlib import pyplot as plt
import peakutils

def DTMF(signal, rate):
    #dictionary baray inke batavajo be freq ha betonim key ke zade shode ro motavaje beshim
    freq_of_keys= { '1': (1209, 697), '2': (1336, 697),'3': (1477, 697), 'A': (1633, 697),'4': (1209, 770),'5': (1336, 770),'6': (1477, 770),
                    'B': (1633, 770),'7': (1209, 852), '8': (1336, 852), '9': (1477, 852), '0': (1336, 941), 
                    'C': (1633, 852), 'D': (1633, 941), '#': (1477, 941), '*': (1209, 941)} 
    #main channel signal ro extract mikonim
    if(signal.ndim!=1):
        signal = signal[:, 0]
    #tabdil fourie ra ba estefade az  fft mohasebe mikonim
    fourier_transform = np.fft.fft(signal)
    #hamchenin freq hay nazir be nazir an ra ham ba estefade az fft.fftfreq mohasebe mikonim
    frequencies = np.fft.fftfreq(len(signal) , 1/ rate)
    #bayad freq hayi ke be ezey anha tabdil fourie ma peak zade ro bedast biyarim
    #be hamin manzor az peakutils estefade mikonim ta index maghadiri ke peak zadn ro bedast biyarim
    #ke khoroji listi az index ha mibashad
    indexes = peakutils.indexes(fourier_transform, thres=0.02/max(fourier_transform), min_dist=100)
    #az an jaii ke in index ha teadashon ziyade, ma faghat ba onaii kar darim ke to range freq hayi hastan ke key hay ma daran
    #pas az 2 ta list estefade mikonim ke freq hay bala , paien ro to yek baze mahdod dashte bashim
    freq_inRange_low = []
    freq_inRange_high = []
    for i in indexes:
        if( 500<frequencies[i]<1000):
            freq_inRange_low.append(int(frequencies[i]))
        if( 1100<frequencies[i]<1800):
            freq_inRange_high.append(int(frequencies[i]))
    #meghdar delta nabayad az yek hadi bozorgtar bashe ke hichvaght meghdarsh taghir nakone az tarfi
    #nabayad ham kheili kochak bashe ke baes khata dar marahek baad beshe 
    #ba azmoon va khata benazar omad ke 100 meghdar monasebiye
    delta =100
    ans = 0
    #hame freq hayi ke bayad barrasi shavan faseleshon ta freq hay mordenazar ma moghayese mishe 
    #ta oni ke bahash kamtarin fasele ro dare peyda konim
    #in low freq mast
    for item in freq_inRange_low:
        for f in [697, 770, 852, 941]:
            if abs(item-f) < delta :
                delta = abs(item-f)
                ans = f
    freq_max_amp2 = ans
    #inja ham daghgighan mesle marhale ghable faghat inbar darim high freq ro peida mikonim
    delta = 100
    ans = 0
    for item in freq_inRange_high:
        for f in [1209, 1336, 1477, 1633]:
            if abs(item-f) < delta and abs(abs(item-f) - delta)>1 :
                delta = abs(item-f)
                ans = f
    freq_max_amp1= ans
    result=''
    #dar akhar ham to dictionary check mikonim ba in sharayet key mon chi mitone bashe va ono return mikonim
    for key ,value in freq_of_keys.items():
        if(value[0] == freq_max_amp1 and value[1]==freq_max_amp2):
            result = key
    return result