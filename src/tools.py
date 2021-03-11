import os
import numpy as np

jumpThreshold = 40
valueLimit = 250

#Calculate the value of a point preprocessed
def getKnnForwardMean(dataList, index, k):
    i = 0
    sumK = 0.0
    while i < k:
        sumK = sumK + dataList[index-i]
        i = i + 1
        if i > index:
            break
    meanK = sumK/k
    return meanK

#Transform a raw list to a smoother list
def getSmoothedList(dataList, k):
    index = k - 1
    smoothedList = []
    while index < len(dataList):
        smoothedList.append(getKnnForwardMean(dataList, index, k))
        index = index + 1
    return smoothedList

#Get the data in buffer area smoothed
def getSmoothedData(bufferList, k):
    i = 0
    channelNum = len(bufferList[0])
    sortedBufferData = []
    smoothedBufferData = []
    while i < channelNum:
        sortedBufferData.append([])
        smoothedBufferData.append([])
        i = i + 1
    j = 0
    while j < channelNum:
        for data in bufferList:
            sortedBufferData[j].append(data[j])
        smoothedBufferData[j].extend(getSmoothedList(sortedBufferData[j], k))
        j = j + 1
    return smoothedBufferData

def knnForwardRegression(rawData, k):
    index = 0
    smoothData = []
    while index < len(rawData):
        sum = 0.0
        count = 0
        if index < k:
            smoothData.append(float(rawData[index]))
        else:
            while count < k:
                sum = sum + float(rawData[index - count])
                count = count + 1
            smoothData.append(sum/k)
        index = index + 1
    return smoothData

#Judge whether recording should start
def startReading(bufferList, k, n):
    smoothedData = getSmoothedData(bufferList, k)
    channelNum = len(smoothedData)
    bufferLength = len(bufferList)
    i = 0
    if len(bufferList) < k+n:
        return False
    else:
        while i < channelNum:
            latestPoint = smoothedData[i][bufferLength-k]
            previousNPointsMean = (sum(smoothedData[i])-latestPoint)/n
            if latestPoint - previousNPointsMean >= jumpThreshold and latestPoint < valueLimit:
                break
            else:
                i = i + 1
        if i == channelNum:
            return False
        else:
            return True

#For plot
def generateX(n):
    i = 1
    x = []
    while i <= n:
        x.append(i)
        i = i + 1
    x = list(x)
    return x

def labelSwitch(arg):
    switcher = {
        'lr': 0,
        'rr': 1,
        'lw': 2,
        'rw': 3,
        'fi': 4
    }
    return switcher[arg]


def getNormInfo(matArray):
    meanArray = np.mean(matArray,0)
    stdArray = np.std(matArray,0)

    return meanArray, stdArray

def standardise(matArray,meanValue,stdValue):
    standardisedArray = np.zeros((matArray.shape[0], matArray.shape[1]))
    
    for i in range(matArray.shape[0]):
        for j in range(matArray.shape[1]):
            if stdValue[j] == 0:
                print('Bugs in standardisation') ### less chance happen
            else:
                standardisedArray[i,j] = matArray[i,j]-meanValue[j]/stdValue[j]
    return standardisedArray

# class normInfo()


if __name__ == "__main__":
    trainList =[[1,2,3],[4,5,6],[7,8,9],[11,12,13],[11,12,13],[11,12,13]]
    testList = [0,0,0]
    trainArray = np.array(trainList)
    testArray = np.array(testList)
    num1,num2 = getNormInfo(trainArray)
    num1=list(num1)
    print(len(num1))
    # print(np.subtract(testArray,num1)/num2)
    # print(standardise(trainArray))
