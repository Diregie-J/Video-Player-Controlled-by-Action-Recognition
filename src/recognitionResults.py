import os
from ML_Models import neuralNetwork as nn 
import numpy as np

motionList = ['left rotate', 'right rotate', 'left wave', 'right wave', 'fist', 'no motion']

def printResults(featureVector, model):
    predictResult = nn.nnClassifier(featureVector, model)
    if np.max(predictResult)>0.5:
        motionIndex = int(np.argmax(predictResult))
    else:
        motionIndex = 5
    result = "%s" %(motionList[motionIndex])

    # result=1
    print('###########')
    print(result)
    print('###########')
    
    f=open('result.txt','w')
    f.write(str(result))
    f.close()

    return predictResult.tolist()

def printResultsCNN(rawSignal, model):
    predictResult = nn.cnnClassifier(rawSignal, model)
    if np.max(predictResult) > 0.5:
        motionIndex = int(np.argmax(predictResult))
    else:
        motionIndex = 5
    result = "%s is detected." % (motionList[motionIndex])

    # result=1
    print('###########')
    print(result)
    print('###########')
    
    return predictResult.tolist()





def printOutput(data):
    return motionList[data[0]]