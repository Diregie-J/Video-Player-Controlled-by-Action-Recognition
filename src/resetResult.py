import time

while True:
    f = open("test.txt", "r")
    data = f.readline()
    f.close()
    if data != 'no motion':
        time.sleep(2)
        f = open("test.txt", "w")
        f.write('no motion')
        f.close()

