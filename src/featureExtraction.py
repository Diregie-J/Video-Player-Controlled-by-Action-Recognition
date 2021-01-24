import os
import numpy as np

#This file is to calculate the feature matrix of a 3-channel signal segment. 

def getFeatureVector(signalSeg):
    featureVector = []
    for sig in signalSeg:
        timeDomainFeature = [max(sig), min(sig), np.mean(sig), np.var(sig), np.std(sig, ddof=1)]
        frequentDomainFeature = []
        featuresForOneChannel = timeDomainFeature
        featuresForOneChannel.extend(frequentDomainFeature)
        featureVector.extend(featuresForOneChannel)
    return featureVector