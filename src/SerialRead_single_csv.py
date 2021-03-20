'''记录实时数据并放入csv
arduino code使用./src/arduino/real-time/realtime.ino'''


import serial
import time
import sys
from time import sleep
import vis
import os
import signal


def decide_filename(action: str) -> str:
    i = 0

    while os.path.exists(os.path.join(os.getcwd(), action, action + str(i) + ".csv")):
        i += 1

    if i == 0:
        os.mkdir(os.path.join(os.getcwd(), action))

    return os.path.join(os.getcwd(), action, action + str(i) + ".csv")


# change filename, port number, and baudrate if needed
print(os.path.abspath('.'))
port = "COM9"
baudrate = 19200
ser = serial.Serial(port, baudrate)


### 记录10次也即10个csv，每个csv 300行 -- 视情况修改
recordTimes = 10
recordLength = 300


fileCount = 0
filename = './src/'+'rw'+str(fileCount)+'.csv'
f = open(filename, 'w')

print('5秒后开始记录数据，看到start后开始做动作')
sleep(3)
ser.flushInput()
ser.flushOutput()
sleep(2)
print('Start:')
try:
    for fileCount in range(recordTimes):
        filename = './src/'+'rw'+str(fileCount)+'.csv'
        f = open(filename, 'w')
        for recordCount in range(recordLength):
            data = ser.readline()
            # bytes --> string
            data = data.decode()
            # Separate strings with “ ”
            data = data.split(" ")
            # string --> float
            data = list(map(float, data))

            if len(data) != 3:
                print('Invalid row -- discarded')
                continue
            
            f.write(str(data[0]))
            f.write(',')
            f.write(str(data[1]))
            f.write(',')
            f.write(str(data[2]))
            f.write('\n')

        print('休息2秒')
        sleep(2)
        print('Start:')
        fileCount += 1
        
    vis.visFile(filename)
except KeyboardInterrupt:
    vis.visFile(filename)
