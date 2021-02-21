import os
import numpy as np
import math
from scipy import signal
from scipy.fft import fft, ifft, fftfreq


#This file is to calculate the feature matrix of a 3-channel signal segment. 

def getFeatureVector(signalSeg):
    featureVector = []
    for sig in signalSeg:
        mav=0
        wl=0
        ssc=0
        rms=0
        meanFreq=0.0
        medianFreq=0.0
        meanPower=0.0
        vcf=0.0

        # temporary variables
        fs=100
        T=1/fs
        sscThreshold=0
        abs_sum_temp=0
        ssc_temp=0
        rms_temp=0
        freq_temp, psd_temp = signal.welch(sig, fs)
        nominatorValue_temp=0
        denominatorValue_temp=0
        sm2_temp=0
        

        for i in range(len(sig)):
            abs_sum_temp += abs(int(sig[i]))
            rms_temp += sig[i]

            if(i>0):
                wl += abs(int(sig[i]) - int(sig[i-1]))
            if(i>1):
                ssc_temp = (int(sig[i-1]) - int(sig[i-2])) * (int(sig[i-1]) - int(sig[i]))
                if ssc_temp >= sscThreshold:
                    ssc += 1
        mav = abs_sum_temp/len(sig)
        rms = math.sqrt(rms_temp/len(sig))

        for j in range(len(freq_temp)):
            nominatorValue_temp += freq_temp[j]*psd_temp[j]
            denominatorValue_temp += psd_temp[j]
            sm2_temp += np.square(freq_temp[j])*psd_temp[j]

        meanFreq = nominatorValue_temp/denominatorValue_temp
        medianFreq = freq_temp[np.argsort(psd_temp)[len(psd_temp)//2]]
        meanPower = denominatorValue_temp/len(freq_temp)
        vcf = sm2_temp/denominatorValue_temp - np.square(nominatorValue_temp/denominatorValue_temp)

        timeDomainFeature = [mav, wl, ssc, rms]
        frequentDomainFeature = [meanFreq, medianFreq, meanPower, vcf]

        featuresForOneChannel = timeDomainFeature
        featuresForOneChannel.extend(frequentDomainFeature)
        featureVector.extend(featuresForOneChannel)
    return featureVector