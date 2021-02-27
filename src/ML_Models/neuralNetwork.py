import os
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam, RMSprop
from keras.layers import Conv1D, BatchNormalization
from keras.utils import np_utils, normalize
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def nnClassifier(featureVector, model):
    # print(os.path.abspath('.'))

    rtSample = np.array(featureVector).reshape(1, len(featureVector))

    predictResult = model.predict(rtSample)
    print(predictResult)
    for i in range(predictResult.shape[1]):
        if(predictResult[0][i] == 1):
            return int(i)
        else:
            return np.argmax(predictResult)


def cnnClassifier(raw_signal, model):
    raw_signal_stack = np.vstack(np.array(raw_signal))

    predictResult = model.predict(raw_signal_stack)
    for i in range(predictResult.shape[1]):
        if(predictResult[0][i] == 1):
            return int(i)
        else:
            return 0
