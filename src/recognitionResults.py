import os
from ML_Models import neuralNetwork as nn 

motionList = ['no motion', 'down', 'up', 'left', 'right', 'fist']

def printResults(featureVector, model):
    motionIndex = nn.nnClassifier(featureVector, model)
    result = "%s is detected." %(motionList[motionIndex])

    # result=1
    print('###########')
    print(result)
    print('###########')