import os
import glob
import pandas as pd
import numpy as np
import math
from scipy import signal
from scipy.fft import fft, ifft, fftfreq


#This file is to calculate the feature matrix of a 3-channel signal segment. 

def prep_highpass(sig):
    b, a = signal.butter(3, 3/50, 'highpass')
    w, h = signal.freqs(b,a)
    # plt.semilogx(w, 20 * np.log10(abs(h)))

    filtered = signal.filtfilt(b,a,sig)
    
    # fft_filtered = fft(filtered)
    # plt.plot(abs(fft_filtered))
    return filtered

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
        if denominatorValue_temp==0:
            print('divide by zero problem -- causing meanFreq and vcf invalid')
            meanFreq=0
            vcf=0

        timeDomainFeature = [mav, wl, ssc, rms]
        frequentDomainFeature = [meanFreq, meanPower, vcf]

        featuresForOneChannel = timeDomainFeature
        featuresForOneChannel.extend(frequentDomainFeature)
        featureVector.extend(featuresForOneChannel)
    return featureVector


if __name__ == "__main__":
    emg_1_csv={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
    emg_2_csv={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
    emg_3_csv={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
    actionList = ['d', 'u', 'l', 'r', 'f']

    folderPath_hyq = os.path.abspath('./src/Dataset/new/hyqData/testOnly')
    filePathList=[]
    filePathList.append(glob.glob(os.path.join(folderPath_hyq, "*.csv")))

    for filePathListIndex in filePathList:
        csvData={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
        dl=[]
        for f in filePathListIndex:
            csvData[f[-5]] = pd.read_csv(f, header=None).values.tolist()
    for actionIndex in actionList:
        for row in range(len(csvData[actionIndex])):
            emg_1_csv[actionIndex].append(csvData[actionIndex][row][0])
            emg_2_csv[actionIndex].append(csvData[actionIndex][row][1])
            emg_3_csv[actionIndex].append(csvData[actionIndex][row][2])

    # print(len(emg_1_csv['f']))
    for i in range(0,3):
        sig=[[],[],[]]
        sig[0]=(emg_1_csv['f'][(i-1)*300+50:(i-1)*300+150])
        sig[1]=(emg_2_csv['f'][(i-1)*300+50:(i-1)*300+150])
        sig[2]=(emg_3_csv['f'][(i-1)*300+50:(i-1)*300+150])
        print(getFeatureVector(sig))