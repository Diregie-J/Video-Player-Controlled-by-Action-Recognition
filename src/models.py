import tensorflow as tf
import matplotlib as plt
from tensorflow import keras
from tensorflow.keras import *
from tensorflow.keras.layers import *


def cnn_(layers_num, f, k, a):
    backend.clear_session()

    model = Sequential()
    model.add(Conv1D(filters=f, kernel_size=k,
                     activation=a, input_shape=x_train.shape[1:]))
    model.add(MaxPooling1D(pool_size=2, strides=1, padding='valid'))

    for _ in range(layers_num):
        model.add(Conv1D(filters=f,
                         kernel_size=k, activation=a))

    model.add(Conv1D(filters=f,
                     kernel_size=k, activation=a))
    model.add(MaxPooling1D(pool_size=2, strides=1, padding='valid'))
    model.add(Flatten())
    model.add(Dense(6, activation='softmax'))

    model.summary()

    opt = RMSprop(lr=0.0001, decay=1e-6)

    model.compile(loss='categorical_crossentropy',
                  optimizer=opt, metrics=['accuracy'])

    history = model.fit(x_train, y_train_class, batch_size=32, epochs=20)
    score = model.evaluate(x_test, y_test_class, verbose=0)

    return history.history['accuracy'][-1], score[1]
