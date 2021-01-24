import serial
import time
import sys
from time import sleep
import vis

filename = 'fist'+'15'+'.csv'
port = "COM9"
baudrate = 19200

ser = serial.Serial(port, baudrate)
ser.set_buffer_size(rx_size = 2147483647, tx_size = 2147483647)

# b'0.13\r\n'

# with open(filename, 'a') as data_file:
#     while True:
#         sleep(1)
#         x1 = ser.readline()#.strip().decode('utf-8')
#         x2 = ser.readline()#.strip().decode('utf-8')
#         x3 = ser.readline()#.strip().decode('utf-8')
#         data_file.write(str(x1))
#         data_file.write(',')
#         data_file.write(str(x2))
#         data_file.write(',')
#         data_file.write(str(x3))
#         data_file.write(',')
#         data_file.write('1\n')

# time1=0
# sum=0
#
# for i in range(100):
#
#     time1 = time.time()
#     temp11=ser.readline()#.strip().decode('utf-8')
#     temp12=ser.readline()#.strip().decode('utf-8')
#     temp13=ser.readline()#.strip().decode('utf-8')
#     time2 = time.time() - time1
#     print(time2)
#     sum = sum+time2
#
# print(sum/100)


#info = b"a\r\n"

# ser.write(info.encode('utf-8'))

# ser.write(bytes(b'a'))

sleep(2)

ser.flushInput()
ser.flushOutput()
ser.write("a".encode())
print("Start")
sleep(0.01)
f = open(filename, 'w')

i=0
for i in range(300):
    #ser.write(bytes(b'a'))
    #ser.write(bytes(b'a'))


    #print(ser.readline())
    #print(ser.readline())


    time1 = time.time()
    f.write(str(ser.readline().strip().decode('utf-8')))
    f.write(',')
    f.write(str(ser.readline().strip().decode('utf-8')))
    f.write(',')
    f.write(str(ser.readline().strip().decode('utf-8')))
    f.write(',')
    f.write(str(ser.readline().strip().decode('utf-8')))
    f.write('\n')


    f.close()
    f = open(filename, 'a')
    #time2=time.time()-time1
    #print(time2)

vis.visFile(filename)