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
    result = "%s is detected." %(motionList[motionIndex])

    # result=1
    print('###########')
    print(result)
    print('###########')
    return predictResult.tolist()

def printSVMResults(featureVector, model):
    predictResult = model.predict(featureVector)
    print(predictResult)
    # result = "%s is detected." %(motionList[predictResult])

    # # result=1
    # print('###########')
    # print(result)
    # print('###########')
    # return predictResult.tolist()