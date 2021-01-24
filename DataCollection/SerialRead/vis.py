import csv
from matplotlib import pyplot as plt

def visFile(filename):
    with open(filename) as f:
        reader = csv.reader(f)

        channel_1 = []
        channel_2 = []
        channel_3 = []

        for row in reader:
            ch_1 = int(row[0])
            ch_2 = int(row[1])
            ch_3 = int(row[2])
            channel_1.append(ch_1)
            channel_2.append(ch_2)
            channel_3.append(ch_3)

    fig=plt.figure(dpi=128,figsize=(10,6))
    plt.plot(channel_1,c='red')
    plt.plot(channel_2,c='orange')
    plt.plot(channel_3,c='blue')

    plt.title(filename,fontsize=24)
    plt.xlabel('Samples',fontsize=24)
    plt.ylabel('Sensor Read',fontsize=16)
    plt.tick_params(axis='both',which='major',labelsize=16)
    plt.show()