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
from tools import getSmoothedList, labelSwitch, getNormInfo, standardise
from featureExtraction import getFeatureVector
from model import model_ann
from keras.models import load_model
import recognitionResults as rr

# model = load_model('./src/ML_models/test2.h5')
folderPath = os.path.abspath('./DataSet/newFromRealTime/')
filePathList=[]
data=[]
filePathList.append(glob.glob(os.path.join(folderPath, "*_log.csv")))
csvData={'lr': [] , 'rr': [], 'lw': [], 'rw': [], 'fi': []}
recordLength=300
for filePathListIndex in filePathList:
    for f in filePathListIndex:
        fileName = Path(f).stem
        print(fileName)
        ### skip any specific action
        # if fileName[0:2] =='rr' or fileName[0:2] =='lr':
        #     continue
        data = pd.read_csv(f, header=None).values.tolist() # csv file -> data list (data length) of list (3)
        print(len(data))
        for i in range(0,len(data),recordLength):
            sigSegment=[[],[],[]]
            for j in range(recordLength):
                sigSegment[0].append(data[i+j][0])
                sigSegment[1].append(data[i+j][1])
                sigSegment[2].append(data[i+j][2])
            # print(len(sigSegment[0]))
            # print(sigSegment[0][70:78])
            csvData[fileName[0:2]].append(sigSegment)
            # sigSegment.clear()

'''保证每个动作训练数据量一样'''
'''csvLength=[]
for i in csvData.keys():
    csvLength.append(len(csvData[i]))
print(min(csvLength))
actionLength = min(csvLength)'''

# len(csvData['lr']) -> 动作的次数: 20
# len(csvData['lr'][2]) -> 3
# len(csvData['lr'][0][0]) -> 150
# csvData['lr'][0] - 3x150  -> 150x3
# minimumValue=NaN
# for index in csvData.keys():
#     temp=len(index)
#     if temp<minimumValue:
#         minimumValue=temp

# 划窗

isLog = True
featureMatrix=[]
labelMatrix=[]
featureVector=[]
for index in csvData.keys():
    print(len(csvData[index]))
    if isLog:
        featureLog = './'+index+'_feature.csv'
        fl = open(featureLog, 'w')
    if True:
        actionLength=len(csvData[index])
        for i in range(actionLength):
            featureVector = getFeatureVector(csvData[index][i])
            
            # if len(featureVector)!=21:
            #     print('wrong length -- discarded')
            #     continue
            # print(len(featureVector))
            featureMatrix.append(featureVector)
            labelMatrix.append(labelSwitch(index))
            if isLog:
                for item in featureVector:
                    fl.write(str(item))
                    fl.write(',')
                fl.write(str(index))
                fl.write('\n')
        # if index=='fi':
        #     print(len(featureVector))



featureMatrix = np.array(featureMatrix)
print(featureMatrix.shape)
labelMatrix = np.array(labelMatrix).reshape(len(labelMatrix),1)
print(labelMatrix.shape)
# discard the last row to prevent errors
featureMatrix = featureMatrix[:-1, :]
labelMatrix = labelMatrix[:-1, :]

# standardisation
fileName_info = open('normInfo.csv','w')
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

# normalisation
# featureMatrix = normalize(featureMatrix, axis = 1)

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

# print(x_train[0])
# print(y_train_class.shape)
# print(x_validate.shape)
# print(y_validate_class.shape)
# print(x_test.shape)
# print(y_test_class.shape)
# for i in range(10):
#     print(y_validate_class[i])

model = model_ann(x_train.shape[1:])
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=50, verbose=0, mode='max', baseline=None, restore_best_weights=True)
history=model.fit(x_train, y_train_class, epochs=50, batch_size=100, verbose=1, validation_data=(x_validate, y_validate_class), callbacks=[early_stop])
score = model.evaluate(x_test, y_test_class, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Valid'], loc='upper left')
plt.show()

# Plot training accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Valid'], loc='upper left')
plt.show()



model.save('ann_model.h5')