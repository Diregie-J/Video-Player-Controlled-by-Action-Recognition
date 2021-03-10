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
filename = './src/Dataset/newFromRealTime/'+'rw'+'.csv'
port = "COM9"
baudrate = 19200
ser = serial.Serial(port, baudrate)
# ser.set_buffer_size(rx_size=2147483647, tx_size=2147483647)

# ser.write("a".encode())
f = open(filename, 'w')
print('5秒后开始记录数据，看到start后开始做动作')
sleep(3)
ser.flushInput()
ser.flushOutput()
sleep(2)
print('Start:')
try:
    recordCount = 0
    for recordCount in range(10000):
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

        # sleep(0.01)
        # time1 = time.time()
        f.write(str(data[0]))
        f.write(',')
        f.write(str(data[1]))
        f.write(',')
        f.write(str(data[2]))
        f.write('\n')

        # f.close()
        # f = open(filename, 'a')
        # time2=time.time()-time1
        # print(time2)

        # print("Relax")
        # sleep(3)
    vis.visFile(filename)
except KeyboardInterrupt:
    vis.visFile(filename)
