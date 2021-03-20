import os
import recognitionResults as rr
import serial
import tools
import matplotlib.pyplot as plt
from keras.models import load_model
import numpy as np
import time

# k and n are used to detect whether a motion happens
k = 10
n = 10
winWidth = 200

ser = serial.Serial('COM9', 19200)
f = open('./standardisation.txt', 'r')
mean = f.readline()
mean = float(mean)
std = f.readline()
std = float(std)
model = load_model('./ML_models/cnn.h5')

print(mean)
print(std)

f.close()

if __name__ == '__main__':
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
    # print(signalSegment)
    ser.flushInput()
    ser.flushOutput()
    # Real-time reading
    while True:
        data = ser.readline()
        # bytes --> string
        data = data.decode()
        # Separate strings with “ ”
        data = data.split(" ")
        # string --> float
        data = list(map(float, data))

        if len(data) != 3:
            continue

        # Update buffer list
        if len(bufferList) < k+n:
            bufferList.append(data)
        else:
            bufferList.append(data)
            del bufferList[0]

        # Judge whether to start or end reading
        if not valid:
            if tools.startReading(bufferList, k, n):
                valid = True
                recordOrNot = True
                recordTimesCounter = 0
            if actionModel != 0:
                actionModel = 0
        else:
            if recordTimesCounter >= winWidth:  # means reading is over
                print(np.array(signalSegment).shape)

                signalSegmentArr = (np.array(signalSegment) - mean) / std
                signalSegmentArr = np.transpose(signalSegmentArr)
                print(signalSegmentArr.shape)
                signalSegmentArr= signalSegmentArr.tolist()
                print(np.array(signalSegmentArr).shape)
   

                rr.printResultsCNN(signalSegmentArr, model)
                # Plot signal segment
                segCounter = segCounter + 1
                '''if segCounter == 10:
                        print(len(signalSegment[0]))
                        print(len(tools.generateX(winWidth)))
                        plt.plot(tools.generateX(winWidth), signalSegment[0], color='green', label='channel 1')
                        plt.plot(tools.generateX(winWidth), signalSegment[1], color='red', label='channel 2')
                        plt.plot(tools.generateX(winWidth), signalSegment[2], color='blue', label='channel 3')
                        plt.legend()
                        plt.xlabel('time')
                        plt.ylabel('value')
                        plt.show()'''
                # Save signal segment as csv file
                # path = os.path.join(segCounter, ".csv")
                # with open(path, 'a') as f:
                #     csv_write = csv.writer(f)
                #     for a in signalSegment:
                #         csv_write.writerow(a)
                recordTimesCounter = 0
                valid = False
                recordOrNot = False
                for sigList in signalSegment:
                    sigList.clear()
                # smoothSig.clear()
                bufferList=[]
            # if valid:
            #     print(data)
            #     csv_write.writerow(data)
            #     # Re-initialize status and signal segment
            #     recordTimesCounter = 0
            #     valid = False
            #     recordOrNot = False
            #     for sigList in signalSegment:
            #         sigList = []

        # Read valid data from serial
        if recordOrNot:
            index = 0
            while index < len(signalSegment):
                signalSegment[index].append(data[index])
                index = index + 1
            recordTimesCounter = recordTimesCounter + 1
