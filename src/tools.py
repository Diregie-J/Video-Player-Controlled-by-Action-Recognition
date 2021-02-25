import os

jumpThreshold = 16
valueLimit = 250

#Calculate the value of a point preprocessed
def getKnnForwardMean(dataList, index, k):
    i = 0
    sumK = 0.0
    if index < k-1:
        sumK = dataList[index]
    else:
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
