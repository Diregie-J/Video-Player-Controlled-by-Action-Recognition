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
from keras.models import load_model


def nnClassifier(featureVector):
    print(os.path.abspath('.'))
    model = load_model('./src/ML_models/ann.h5')

    rtSample = np.array(featureVector).reshape(1,len(featureVector))


    predictResult = model.predict(rtSample)
    for i in range(predictResult.shape[1]):
        if(predictResult[0][i] == 1):
            return int(i)
        else:
            return 0