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
from keras.models import load_model
import recognitionResults as rr

# model = load_model('./src/ML_models/test2.h5')
folderPath = os.path.abspath('./src/Dataset/newFromRealTime/hyqData')
filePathList=[]
data=[]
filePathList.append(glob.glob(os.path.join(folderPath, "*.csv")))
csvData={'d': [] , 'u': [], 'l': [], 'r': [], 'f': []}
for filePathListIndex in filePathList:
    for f in filePathListIndex:
        data = pd.read_csv(f, header=None).values.tolist() # csv file -> data list (100) of list (3)
        if len(data) !=300:
            print('Inconsistent length -- check sample length')

        sigSegment=[[],[],[]]
        for i in range(len(data)):
            sigSegment[0].append(data[i][0])
            sigSegment[1].append(data[i][1])
            sigSegment[2].append(data[i][2])
        # print(f[114])
        # f[114] -- filename
        csvData[f[114]].append(sigSegment)
        featureVector = getFeatureVector(sigSegment)



        # print(getFeatureVector(sigSegment))


        # rr.printResults(featureVector, model)
featureMatrix=[]
labelMatrix=[]
for keyname in csvData.keys():
    for row in range(len(csvData[keyname])):
        featureVector=getFeatureVector(csvData[keyname][row])
        featureMatrix.append(featureVector)
        labelMatrix.append(labelSwitch(keyname))

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

print(x_train[0])
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

early_stop = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=5, verbose=0, mode='max', baseline=None, restore_best_weights=True)
history=model.fit(x_train, y_train_class, epochs=100, batch_size=100, verbose=1, validation_data=(x_validate, y_validate_class), callbacks=[early_stop])
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



model.save('test2.h5')