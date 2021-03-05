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

#k and n are used to detect whether a motion happens
k = 10
n = 10
winWidth = 150

# model = load_model('./src/ML_models/test2.h5')
# model_cnn = load_model('./src/ML_models/cnn.h5')


# port = "COM9"
# baudrate = 19200
# ser = serial.Serial(port, baudrate)

print(os.path.abspath('.'))
folderPath = os.path.abspath('.')
fileName = './src/temp.csv'


if True: #__name__ == '__main__':
    time.sleep(1)
    smoothSig=[]
    valid = False
    recordOrNot = False
    numOfChannel = 3
    # len(ser.readline().decode().split(" "))
    signalSegment = []
    bufferList = []
    recordTimesCounter = 0
    actionModel = 0
    resetCom = 0
    segCounter = 0

    # initialize valid signal segment
    counter = 0
    while counter < numOfChannel:
        signalSegment.append([])
        counter = counter + 1
    

    # Read csv
    dataFromCSV = []
    with open(fileName, newline='') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            # print(row)
            row_float=[float(i) for i in row]
            dataFromCSV.append(row_float)


    for data in dataFromCSV:
        if len(data) != 3:
            continue
        #Update buffer list
        if len(bufferList) < k+n:
            bufferList.append(data)
        else:
            bufferList.append(data)
            del bufferList[0]

        #Judge whether to start or end reading
        if not valid:
            if tools.startReading(bufferList, k, n):
                valid = True
                recordOrNot = True
                recordTimesCounter = 0
            if actionModel != 0:
                actionModel = 0
        else:
            if recordTimesCounter >= winWidth: #means reading is over
                for sig in signalSegment:
                    smoothSig.append(tools.knnForwardRegression(sig,k))
                # print(len(smoothSig[0]))
                # path = os.path.join(os.getcwd(),'uu'+str(segCounter)+".csv")
                # f = open(path, 'w')
                # for i in range(len(signalSegment[2])):
                #     f.write(str(signalSegment[0][i]))
                #     f.write(',')
                #     f.write(str(signalSegment[1][i]))
                #     f.write(',')
                #     f.write(str(signalSegment[2][i]))
                #     f.write('\n')
                #     f.close()
                #     f = open(path, 'a')

                #Get feature vector
                # featureVector = feature.getFeatureVector(smoothSig)
                
                # #Get recognition result
                # rr.printResults(featureVector, model)
                # rr.printResults(signalSegment, model_cnn)
                
                #Plot signal segment
                segCounter = segCounter + 1
                if True:
                    # print(len(tools.generateX(winWidth)))
                    plt.plot(tools.generateX(winWidth), smoothSig[0], color='blue', label='channel 1')
                    plt.plot(tools.generateX(winWidth), smoothSig[1], color='orange', label='channel 2')
                    plt.plot(tools.generateX(winWidth), smoothSig[2], color='green', label='channel 3')
                    plt.legend()
                    plt.xlabel('time')
                    plt.ylabel('value')
                    plt.show()
                # path = os.path.join(os.getcwd(),str(segCounter)+".csv")
                # with open(path, 'a') as f:
                #     csv_write = csv.writer(f)        
                #     for a in signalSegment:
                #         csv_write.writerow(a)
            
                #Re-initialize status and signal segment
                recordTimesCounter = 0
                valid = False
                recordOrNot = False
                for sigList in signalSegment:
                    sigList.clear()
                smoothSig.clear()
                bufferList=[]
                
        
        #Read valid data from serial
        if recordOrNot:
            index = 0
            while index < len(signalSegment):
                signalSegment[index].append(data[index])
                index = index + 1
            recordTimesCounter = recordTimesCounter + 1