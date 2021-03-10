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

def model_ann(xShape):
    model = Sequential()
    model.add(Dense(48, activation='relu', kernel_initializer='he_normal', input_shape=xShape))
    # model.add(BatchNormalization())
    # model.add(Dense(128, activation='relu', kernel_initializer='he_normal', input_shape=xShape))
    model.add(Dense(5, activation='softmax'))

    return model