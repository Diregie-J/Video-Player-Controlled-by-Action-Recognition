import csv
import glob, os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import signal
from scipy.fft import fft, ifft, fftfreq, fftshift
import random
from tools import getSmoothedList
from featureExtraction import getFeatureVector

print(os.path.abspath('.'))
# csv reader (faster)
emg_1_csv={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
emg_2_csv={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
emg_3_csv={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
actionList = ['d', 'u', 'l', 'r', 'f']


folderPath_hyq = os.path.abspath('./src/Dataset/new/hyqData/')
folderPath_zjh = os.path.abspath('./src/Dataset/new/zjhData/')
folderPath_sgf = os.path.abspath('./src/Dataset/new/sgfData/')

filePathList=[]
filePathList.append(glob.glob(os.path.join(folderPath_hyq, "*.csv")))
filePathList.append(glob.glob(os.path.join(folderPath_zjh, "*.csv")))
filePathList.append(glob.glob(os.path.join(folderPath_sgf, "*.csv")))

for filePathListIndex in filePathList:
    csvData={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
    dl=[]
    # print('Reading .csv:')
    for f in filePathListIndex:
        csvData[f[-5]] = pd.read_csv(f, header=None).values.tolist()
        # print(f[-5])
    for actionIndex in actionList:
        for row in range(len(csvData[actionIndex])):
            emg_1_csv[actionIndex].append(csvData[actionIndex][row][0])
            emg_2_csv[actionIndex].append(csvData[actionIndex][row][1])
            emg_3_csv[actionIndex].append(csvData[actionIndex][row][2])

# windowing
record_length=300
window_length=120
window_slice=[50]
# window_slice = [m for m in range(10,51,1)]


emg_1_window={'d': {} , 'u': {}, 'l': {}, 'r': {}, 'f': {}}
emg_2_window={'d': {} , 'u': {}, 'l': {}, 'r': {}, 'f': {}}
emg_3_window={'d': {} , 'u': {}, 'l': {}, 'r': {}, 'f': {}}
sigSegment=[[],[],[]]
sigList=[]
sigLabel=[]

for actionIndex in range(len(actionList)):
    print('Windowing: ' + actionList[actionIndex])
  
    emg_1_slice = [emg_1_csv[actionList[actionIndex]][i:i+record_length] for i in range(0,len(emg_1_csv[actionList[actionIndex]]),record_length)]
    emg_2_slice = [emg_2_csv[actionList[actionIndex]][i:i+record_length] for i in range(0,len(emg_2_csv[actionList[actionIndex]]),record_length)]
    emg_3_slice = [emg_3_csv[actionList[actionIndex]][i:i+record_length] for i in range(0,len(emg_3_csv[actionList[actionIndex]]),record_length)]

    print(len(emg_1_slice))
    print(len(emg_2_slice))
    print(len(emg_3_slice))

    generatedIndex=0
    for i in range(len(emg_1_slice)):
        max_1 = emg_1_slice[i].index(max(emg_1_slice[i]))
        max_2 = emg_2_slice[i].index(max(emg_2_slice[i]))
        max_3 = emg_3_slice[i].index(max(emg_3_slice[i]))
        avgMax=int((max_1+max_2+max_3)/3)
        
        for window_slice_index in range(len(window_slice)):

            # if max_1>window_slice[window_slice_index] and max_1<record_length-window_slice[window_slice_index] and max_2>window_slice[window_slice_index] and max_2<record_length-window_slice[window_slice_index] and max_3>window_slice[window_slice_index] and max_3<record_length-window_slice[window_slice_index]:
            if avgMax>window_slice[window_slice_index] and avgMax<record_length-window_length+window_slice[window_slice_index]:
                emg_1_window[actionList[actionIndex]][generatedIndex] = emg_1_slice[i][avgMax-window_slice[window_slice_index]:avgMax+(window_length-window_slice[window_slice_index])]
                emg_2_window[actionList[actionIndex]][generatedIndex] = emg_2_slice[i][avgMax-window_slice[window_slice_index]:avgMax+(window_length-window_slice[window_slice_index])]
                emg_3_window[actionList[actionIndex]][generatedIndex] = emg_3_slice[i][avgMax-window_slice[window_slice_index]:avgMax+(window_length-window_slice[window_slice_index])]
                sigSegment[0]=emg_1_window[actionList[actionIndex]][generatedIndex]
                sigSegment[1]=emg_2_window[actionList[actionIndex]][generatedIndex]
                sigSegment[2]=emg_3_window[actionList[actionIndex]][generatedIndex]
                sigList.append(sigSegment)
                sigLabel.append(actionList[actionIndex])
                generatedIndex+=1

# plot an example
# plt.plot(emg_1_window['d'][0])
# plt.plot(emg_2_window['d'][0])
# plt.plot(emg_3_window['d'][0])
# plt.legend(['Channel 1', 'Channel 2', 'Channel 3'])
# plt.xlabel('Samples')
# plt.ylabel('ADC Value')
# plt.grid()
# plt.show()


# feature extraction
featureMatrix=[]
for i in range(len(sigList)):
    feature=getFeatureVector(sigList[0])
    featureMatrix.append(feature)

featureMatrix = np.array(featureMatrix)
print(featureMatrix.shape)
labelMatrix = np.array(sigLabel).reshape(len(sigLabel),1)
print(labelMatrix.shape)

# feat