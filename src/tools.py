import os

jumpThreshold = 50
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
        'd': 1,
        'u': 2,
        'l': 3,
        'r': 4,
        'f': 5
    }
    return switcher[arg]