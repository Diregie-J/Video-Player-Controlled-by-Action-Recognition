import os
from ML_Models import neuralNetwork as nn 

motionList = ['left rotate', 'right rotate', 'left wave', 'right wave', 'fist']

def printResults(featureVector, model):
    motionIndex = nn.nnClassifier(featureVector, model)
    result = "%s is detected." %(motionList[motionIndex])

    # result=1
    print('###########')
    print(result)
    print('###########')