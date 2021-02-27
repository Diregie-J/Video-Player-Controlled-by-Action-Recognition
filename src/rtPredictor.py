import os
import featureExtraction as feature 
import recognitionResults as rr 
import serial
import tools
import matplotlib.pyplot as plt
import time
from keras.models import load_model
import csv
from tools import getSmoothedList, knnForwardRegression

model = load_model('./src/ML_models/test2.h5')
port = "COM9"
baudrate = 19200
ser = serial.Serial(port, baudrate)

if __name__ == '__main__':
    time.sleep(1)
    smoothSig=[]
    valid = False
    recordOrNot = False
    
    winWidth=100
    dynamic = 10
    dynamicThreshold = 5
    baseMean_ch1=0
    baseMean_ch2=0
    baseMean_ch3=0
    bufferSize = 300
    bufferList = []
    signalSegment = [[],[],[]]
    

    counter = 0

    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)


    # for i in range(bufferSize):
    #     data = ser.readline()
    #     #bytes --> string
    #     data = data.decode() 
    #     #Separate strings with “ ”
    #     data = data.split(" ") 
    #     #string --> float
    #     data = list(map(float, data))
    #     if len(data) != 3:
    #         continue
    #     bufferList.append(data)


    #initialize valid signal segment

    print('Start:')
    while True:
        data = ser.readline()
        #bytes --> string
        data = data.decode() 
        #Separate strings with “ ”
        data = data.split(" ") 
        #string --> float
        data = list(map(float, data))

        if len(data) != 3:
            continue
        if len(bufferList) < bufferSize:
            bufferList.append(data)
        else:
            bufferList.append(data)
            del bufferList[0]
        
        if len(bufferList) == bufferSize:
            if not valid:
                for i in range(bufferSize):
                    baseMean_ch1 += bufferList[i][0]
                    baseMean_ch2 += bufferList[i][1]
                    baseMean_ch3 += bufferList[i][2]
                baseMean_ch1 = baseMean_ch1/bufferSize
                baseMean_ch2 = baseMean_ch2/bufferSize
                baseMean_ch3 = baseMean_ch3/bufferSize
                # print(baseMean_ch1)
                # print(baseMean_ch2)
                # print(baseMean_ch3)
                dynamicMean_ch1=0
                dynamicMean_ch2=0
                dynamicMean_ch3=0
                for i in range(dynamic):
                    dynamicMean_ch1 += bufferList[bufferSize-1-i][0]
                    dynamicMean_ch2 += bufferList[bufferSize-1-i][1]
                    dynamicMean_ch3 += bufferList[bufferSize-1-i][2]
                dynamicMean_ch1 = dynamicMean_ch1/dynamic
                dynamicMean_ch2 = dynamicMean_ch2/dynamic
                dynamicMean_ch3 = dynamicMean_ch3/dynamic
                if dynamicMean_ch1 > baseMean_ch1 and dynamicMean_ch2 > baseMean_ch2 and dynamicMean_ch3 > baseMean_ch3:
                    counter+=1
                    print(counter)
                    recordTimesCounter = 0
                    valid = True
            else:
                if recordTimesCounter == winWidth:
                    
                    # plt.plot(signalSegment[0], color='blue', label='channel 1')
                    # plt.plot(signalSegment[1], color='orange', label='channel 2')
                    # plt.plot(signalSegment[2], color='green', label='channel 3')
                    # plt.legend()
                    # plt.xlabel('time')
                    # plt.ylabel('value')
                    # plt.show()
                    featureVector = feature.getFeatureVector(signalSegment)
                    rr.printResults(featureVector, model)

                    time.sleep(1)
                    valid = False
                    recordTimesCounter = 0
                    signalSegment=[[],[],[]]
                    


        elif len(bufferList) > bufferSize:
            print('Buffer overflow')
            break
        
        if valid:
            for i in range(3):
                signalSegment[i].append(data[i])
            recordTimesCounter+=1

