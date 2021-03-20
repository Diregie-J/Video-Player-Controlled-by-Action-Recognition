import time

while True:
    f = open("result.txt", "r")
    data = f.readline()
    f.close()
    if data != 'no motion':
        time.sleep(2)
        f = open("result.txt", "w")

        f.write('no motion')
        f.close()

