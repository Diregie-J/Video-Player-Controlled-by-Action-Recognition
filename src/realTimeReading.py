import os
import featureExtraction as feature 
import recognitionResults as rr 
import serial
from keras.models import load_model

model = load_model('./src/ML_models/ann.h5')

jumpThreshold = 50
winWidth = 120
#k and n are used to judge whether a motion happens
k = 30
n = 5

ser = serial.Serial('/dev/cu.usbmodem1454101', 9600)

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
            print(latestPoint - previousNPointsMean)
            if latestPoint - previousNPointsMean >= jumpThreshold:
                break
            else:
                i = i + 1
        if i == channelNum:
            return False
        else:
            return True


if __name__ == '__main__':
    valid = False
    recordOrNot = False
    numOfChannel = len(ser.readline().decode().split(" "))
    signalSegment = []
    bufferList = []
    recordTimesCounter = 0

    #initialize valid signal segment
    counter = 0
    while counter < numOfChannel:
        signalSegment.append([])
        counter = counter + 1
    print(signalSegment)
    
    #Real-time reading
    while True:
        data = ser.readline()
        #bytes --> string
        data = data.decode() 
        #Separate strings with “ ”
        data = data.split(" ") 
        #string --> float
        data = list(map(float, data)) 

        #Update buffer list
        if len(bufferList) < k+n:
            bufferList.append(data)
        else:
            bufferList.append(data)
            del bufferList[0]

        #Judge whether to start or end reading
        if not valid:
            if startReading(bufferList, k, n):
                valid = True
                recordOrNot = True
                recordTimesCounter = 0
        else:
            if recordTimesCounter > winWidth: #means reading is over
                #Get feature vector
                featureVector = feature.getFeatureVector(signalSegment)
                #Get recognition result
                rr.printResults(featureVector)
                #Re-initialize status and signal segment
                recordTimesCounter = 0
                valid = False
                recordOrNot = False
                for sigList in signalSegment:
                    sigList = []
        
        #Read valid data from serial
        if recordOrNot:
            index = 0
            while index < len(signalSegment):
                signalSegment[index].append(data[index])
                index = index + 1
            recordTimesCounter = recordTimesCounter + 1
                