import serial

ser = serial.Serial('/dev/cu.usbmodem1454101', 9600)

if __name__ == '__main__':
    print('Start reading... \n')
    while True:
        print('in loop...')
        data = ser.readline()
        data = data.decode()
        data = data.split(" ")
        data = list(map(float, data))
        print(data)
    ser.close()