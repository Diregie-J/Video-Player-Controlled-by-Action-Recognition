import os
import featureExtraction as feature 
import recognitionResults as rr 
import serial

startThreshold = 600
endThreshold = 600

ser = serial.Serial('/dev/cu.usbmodem1454101', 9600)

#Whether recording should start
def startReading(dataList):
    numExceedThre = 0
    for value in dataList:
        if value > startThreshold:
            numExceedThre = numExceedThre + 1
    if numExceedThre > 0:
        return True
    else:
        return False

#Whether recording should end 
def endReading(dataList):
    numExceedThre = 0
    for value in dataList:
        if value < endThreshold:
            numExceedThre = numExceedThre + 1
    if numExceedThre < len(dataList):
        return False
    else:
        return True

if __name__ == '__main__':
    valid = False
    recordOrNot = False
    numOfChannel = len(ser.readline().decode().split(" "))
    signalSegment = []
    counter = 0
    while counter < numOfChannel:
        signalSegment.append([])
        counter = counter + 1
    print(signalSegment)
    while True:
        data = ser.readline()
        #bytes --> string
        data = data.decode() 
        #Separate strings with “ ”
        data = data.split(" ") 
        #string --> float
        data = list(map(float, data)) 
        if not valid:
            if startReading(data):
                valid = True
                recordOrNot = True
        else:
            if endReading(data):
                print(signalSegment)
                featureVector = feature.getFeatureVector(signalSegment)
                rr.printResults(featureVector)
                valid = False
                recordOrNot = False
                for sigList in signalSegment:
                    sigList = []
        if recordOrNot:
            index = 0
            while index < len(signalSegment):
                signalSegment[index].append(data[index])
                index = index + 1
                