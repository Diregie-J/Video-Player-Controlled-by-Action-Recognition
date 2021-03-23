import time

motionList = []
delayList = []

for i in range(len(motionList)):
    time.sleep(delayList[i])
    f = open("test.txt", "w+")
    f.write(motionList[i])
    f.close()