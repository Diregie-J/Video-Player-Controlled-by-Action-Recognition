import os 
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam, RMSprop
from keras.layers import Conv1D, BatchNormalization
from keras.utils import np_utils,normalize
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def nnClassifier(rtSample, model):
    # print(os.path.abspath('.'))

    # rtSample = np.array(featureVector).reshape(1,len(featureVector))


    predictResult = model.predict(rtSample)
    print(predictResult)
    return predictResult
    
    # if np.max(predictResult)>0.5:
    #     return int(np.argmax(predictResult))
    # else:
    #     return 5
        
    # for i in range(predictResult.shape[1]):
    #     print(predictResult[0][i])
    #     if(predictResult[0][i] >= 0.8):
    #         return int(i)
        
            
    # return int(np.argmax(predictResult))



def cnnClassifier(raw_signal, model):
    raw_signal_stack = np.array(raw_signal).reshape(1, 100, 3)
    print(raw_signal_stack.shape)
    predictResult = model.predict(raw_signal_stack)
    print(predictResult)
    for i in range(predictResult.shape[1]):
        if(predictResult[0][i] > 0.5):
            return int(i)
    return 0