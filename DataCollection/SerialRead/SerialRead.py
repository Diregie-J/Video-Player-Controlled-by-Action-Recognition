import serial
import time
import sys
from time import sleep
import vis
import os


def decide_filename(action: str) -> str:
    i = 0

    while os.path.exists(os.path.join(os.getcwd(), action, action + str(i) + ".csv")):
        i += 1

    if i == 0:
        os.mkdir(os.path.join(os.getcwd(), action))

    return os.path.join(os.getcwd(), action, action + str(i) + ".csv")


# change filename, port number, and baudrate if needed

filename = 'temp'+'.csv'

port = "COM9"
baudrate = 19200

ser = serial.Serial(port, baudrate)
ser.set_buffer_size(rx_size=2147483647, tx_size=2147483647)

sleep(2)

ser.write("a".encode())



f = open(filename, 'w')


ser.flushInput()
ser.flushOutput()
while 1:
    ser.flushInput()
    ser.flushOutput()
    print("Start")
    sleep(0.01)
    i = 0
    for i in range(300):
        #time1 = time.time()
        f.write(str(ser.readline().strip().decode('utf-8')))
        f.write(',')
        f.write(str(ser.readline().strip().decode('utf-8')))
        f.write(',')
        f.write(str(ser.readline().strip().decode('utf-8')))
        f.write(',')
        f.write('0') # label
        f.write('\n')


        f.close()
        f = open(filename, 'a')
        #time2=time.time()-time1
        #print(time2)

    print("Relax")
    sleep(3)

vis.visFile(filename)
