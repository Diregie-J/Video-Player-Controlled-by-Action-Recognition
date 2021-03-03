import numpy as np


def scale(signals):
    signals = np.array(signals)

    for channel, signal in signals:
        s = np.std(signal)
        u = np.mean(signal)
        signals[channel] = (signal - u) / s

    return signals
