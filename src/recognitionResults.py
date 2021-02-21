import os
from ML_Models import neuralNetwork as nn 

motionList = ['no motion', 'motion_1', 'motion_2', 'motion_3', 'motion_4', 'motion_5']

def printResults(featureVector, model):
    motionIndex = nn.nnClassifier(featureVector)
    result = "%s is detected." %(motionList[motionIndex])
    print(result)