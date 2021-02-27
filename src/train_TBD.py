# NOT finished

import csv
import glob, os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import signal
from scipy.fft import fft, ifft, fftfreq, fftshift
import random
from tools import getSmoothedList, labelSwitch
from featureExtraction import getFeatureVector
from model import model_ann

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
                sigSegment[0]=[]
                sigSegment[1]=[]
                sigSegment[2]=[]
                emg_1_window[actionList[actionIndex]][generatedIndex] = emg_1_slice[i][avgMax-window_slice[window_slice_index]:avgMax+(window_length-window_slice[window_slice_index])]
                emg_2_window[actionList[actionIndex]][generatedIndex] = emg_2_slice[i][avgMax-window_slice[window_slice_index]:avgMax+(window_length-window_slice[window_slice_index])]
                emg_3_window[actionList[actionIndex]][generatedIndex] = emg_3_slice[i][avgMax-window_slice[window_slice_index]:avgMax+(window_length-window_slice[window_slice_index])]
                sigSegment[0]=emg_1_window[actionList[actionIndex]][generatedIndex]
                sigSegment[1]=emg_2_window[actionList[actionIndex]][generatedIndex]
                sigSegment[2]=emg_3_window[actionList[actionIndex]][generatedIndex]
                sigList.append(sigSegment)
                sigLabel.append(labelSwitch(actionList[actionIndex]))
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
    feature=getFeatureVector(sigList[i])
    # print(feature)
    featureMatrix.append(feature)

featureMatrix = np.array(featureMatrix)
# print(featureMatrix[900])
labelMatrix = np.array(sigLabel).reshape(len(sigLabel),1)
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

early_stop = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=100, verbose=0, mode='max', baseline=None, restore_best_weights=True)
history=model.fit(x_train, y_train_class, epochs=10, batch_size=100, verbose=1, validation_data=(x_validate, y_validate_class), callbacks=[early_stop])
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

score = model.evaluate(x_test, y_test_class, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])