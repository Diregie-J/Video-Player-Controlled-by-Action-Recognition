import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import *
from tensorflow.keras.layers import *
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def cnn(layers_num, filters, kernel_size, activation):
    backend.clear_session()

    model = Sequential()
    model.add(Conv1D(filters=filters, kernel_size=kernel_size,
                     activation=activation, input_shape=x_train.shape[1:]))
    model.add(MaxPooling1D(pool_size=2, strides=1, padding='valid'))

    for _ in range(layers_num):
        model.add(Conv1D(filters=filters,
                         kernel_size=kernel_size, activation=activation))

    model.add(Conv1D(filters=filters,
                     kernel_size=kernel_size, activation=activation))
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
