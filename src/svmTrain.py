import csv
import glob, os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from pathlib import Path
from scipy import signal
from scipy.fft import fft, ifft, fftfreq, fftshift
import random
from tools import getSmoothedList, labelSwitch
from featureExtraction import getFeatureVector
from model import model_ann
from keras.models import load_model
import recognitionResults as rr
from sklearn import preprocessing

def addNoise(data, scale):
    mu=0
    sigma=scale
    noise = np.random.normal(mu, sigma, len(data))
    # noise = np.random.gauss(0,scale,len(data))
    augmented_data = data + noise
    # Cast back to same data type
    augmented_data = augmented_data.astype(type(data[0]))
    return augmented_data

def scale(signals):
    signals = np.array(signals)

    # for channel, signal in signals:
    #     s = np.std(signal)
    #     u = np.mean(signal)
    #     signals[channel] = (signal - u) / s

    # return signals
    min_max_scaler = preprocessing.MinMaxScaler()
    return min_max_scaler.fit_transform(signals).tolist()


# model = load_model('./src/ML_models/test2.h5')
# folderPath = os.path.abspath('DataSet/newFromRealTime/hyqData/')
# filePathList=[]
# data=[]
# filePathList.append(glob.glob(os.path.join(folderPath, "*_log.csv")))
# csvData={'lr': [] , 'rr': [], 'lw': [], 'rw': [], 'fi': []}
# recordLength=150
# scales=[0.01, 0.02, 0.1, 0.2, 0.5]
# for filePathListIndex in filePathList:
#     for f in filePathListIndex:
#         fileName = Path(f).stem
#         print(fileName)
#         # if fileName[0:2] =='rr' or fileName[0:2] =='lr':
#         #     continue
#         data = pd.read_csv(f, header=None).values.tolist() # csv file -> data list (data length) of list (3)
#         print(len(data))
#         for i in range(0,len(data),recordLength):
#             sigSegment=[[],[],[]]
#             noiseSig=[[],[],[]]
#             for j in range(recordLength):
#                 sigSegment[0].append(data[i+j][0])
#                 sigSegment[1].append(data[i+j][1])
#                 sigSegment[2].append(data[i+j][2])
#             for k in range(0,len(scales)):
#                 noiseSig[0] = addNoise(sigSegment[0],scales[k])
#                 # pitchSig[0] = pitch(sigSegment[0],100,0.1)
#                 noiseSig[1] = addNoise(sigSegment[0],scales[k])
#                 # pitchSig[1] = pitch(sigSegment[0],100,0.1)
#                 noiseSig[2] = addNoise(sigSegment[0],scales[k])
#                 csvData[fileName[0:2]].append(scale(noiseSig))

#                 noiseSig=[[],[],[]]
#             # pitchSig[2] = pitch(sigSegment[0],100,0.1)
        
#             csvData[fileName[0:2]].append(scale(sigSegment))
#             # sigSegment.clear()
 
 



import csv
import glob, os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from pathlib import Path
from scipy import signal
from scipy.fft import fft, ifft, fftfreq, fftshift
import random
from tools import getSmoothedList, labelSwitch, standardise, getNormInfo
from featureExtraction import getFeatureVector
from model import model_ann
from keras.models import load_model
import recognitionResults as rr

# model = load_model('./src/ML_models/test2.h5')
folderPath = os.path.abspath('./src/DataSet/newFromRealTime/hyqData/')
filePathList=[]
data=[]
filePathList.append(glob.glob(os.path.join(folderPath, "*_log.csv")))
csvData={'lr': [] , 'rr': [], 'lw': [], 'rw': [], 'fi': []}
recordLength = 300
scales=[0.01, 0.02, 0.1, 0.2, 0.5]
for filePathListIndex in filePathList:
    for f in filePathListIndex:
        fileName = Path(f).stem
        print(fileName)
        ### 如果需要，可以简化任务
        # if fileName[0:2] =='rr': #fileName[0:2] =='rr' or 
        #     continue
        data = pd.read_csv(f, header=None).values.tolist() # csv file -> data list (data length) of list (3)
        print(len(data))
        for i in range(0,len(data),recordLength):
            sigSegment=[[],[],[]]
            noiseSig=[[],[],[]]
            for j in range(recordLength):
                sigSegment[0].append(data[i+j][0])
                sigSegment[1].append(data[i+j][1])
                sigSegment[2].append(data[i+j][2])
            for k in range(0,len(scales)):
                noiseSig[0] = addNoise(sigSegment[0],scales[k])
                # pitchSig[0] = pitch(sigSegment[0],100,0.1)
                noiseSig[1] = addNoise(sigSegment[0],scales[k])
                # pitchSig[1] = pitch(sigSegment[0],100,0.1)
                noiseSig[2] = addNoise(sigSegment[0],scales[k])
            # print(len(sigSegment[0]))
            # print(sigSegment[0][70:78])
            csvData[fileName[0:2]].append(sigSegment)
            csvData[fileName[0:2]].append(noiseSig)
            # sigSegment.clear()

'''保证每个动作训练数据量一样'''
csvLength=[]
for i in csvData.keys():
    csvLength.append(len(csvData[i]))
print(min(csvLength))
actionLength = min(csvLength)

# 划窗

isLog = False
featureMatrix=[]
labelMatrix=[]
for index in csvData.keys():
    if isLog:
        featureLog = './src/'+index+'_feature.csv'
        fl = open(featureLog, 'w')
    if True: #index !='rr':
        for i in range(actionLength):
            featureVector = getFeatureVector(csvData[index][i])
            # print(len(featureVector))
            featureMatrix.append(featureVector)
            labelMatrix.append(labelSwitch(index))
            if isLog:
                for item in featureVector:
                    fl.write(str(item))
                    fl.write(',')
                # fl.write()
                fl.write('\n')


featureMatrix = np.array(featureMatrix)
print(featureMatrix.shape)
labelMatrix = np.array(labelMatrix).reshape(len(labelMatrix),1)
print(labelMatrix.shape)

# training the classifier
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam, RMSprop
from keras.layers import Conv1D, BatchNormalization
from keras.utils import np_utils,normalize
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
tf.random.set_seed(1234)

# standardisation
fileName_info = open('./src/normInfo.csv','w')
meanValue, stdValue = getNormInfo(featureMatrix)
featureMatrix = standardise(featureMatrix,meanValue,stdValue)

# save mean and std into a csv for real-time standardisation
meanValue=list(meanValue)
stdValue=list(stdValue)
print(len(meanValue))
for i in range(len(meanValue)-1):
    fileName_info.write(str(meanValue[i]))
    fileName_info.write(',')
fileName_info.write(str(meanValue[i+1]))
fileName_info.write('\n')
for i in range(len(stdValue)-1):
    fileName_info.write(str(stdValue[i]))
    fileName_info.write(',')
fileName_info.write(str(stdValue[i+1]))
fileName_info.close()


state = np.random.get_state()
np.random.shuffle(featureMatrix)
np.random.set_state(state)
np.random.shuffle(labelMatrix)


TRAIN_SPLIT = int(0.6*featureMatrix.shape[0])
TEST_SPLIT = int(0.2*featureMatrix.shape[0] + TRAIN_SPLIT)

x_train, x_test, x_validate = np.split(featureMatrix, [TRAIN_SPLIT, TEST_SPLIT])
y_train, y_test, y_validate = np.split(labelMatrix, [TRAIN_SPLIT, TEST_SPLIT])

y_train_class = np_utils.to_categorical(y_train)
y_test_class = np_utils.to_categorical(y_test)
y_validate_class = np_utils.to_categorical(y_validate)


# print(y_train_class.shape)
# print(x_validate.shape)
# print(y_validate_class.shape)
# print(x_test.shape)
# print(y_test_class.shape)
# for i in range(10):
#     print(y_validate_class[i])
 
from sklearn.svm import SVC
clf = SVC(kernel='linear')
clf.fit(x_train, y_train.ravel())

import joblib
joblib.dump(clf, "svm_model.pkl")
print(clf.predict(x_validate))
# print(y_validate.ravel())

print('Train acc:'+str(clf.score(x_train, y_train))) 
print('Test acc:'+str(clf.score(x_test, y_test)))
