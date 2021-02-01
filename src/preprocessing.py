import csv
import matplotlib.pyplot as plt

#1. plot the raw data
#2. extract valid segment
#3. plot again

path = "rawData/fist.csv"

def knnForwardRegression(rawData, k):
    index = 0
    smoothData = []
    while index < len(rawData):
        sum = 0.0
        count = 0
        if index < k:
            smoothData.append(float(rawData[index]))
        else:
            while count < k:
                sum = sum + float(rawData[index - count])
                count = count + 1
            smoothData.append(sum/k)
        index = index + 1
    return smoothData

if __name__ == '__main__':
    with open(path,"r") as f:
        data = csv.reader(f)
        index = 0
        t = []
        channel_1 = []
        channel_2 = []
        channel_3 = []
        for row in data:
            t.append(index)
            channel_1.append(row[0])
            channel_2.append(row[1])
            channel_3.append(row[2])
            index = index + 1
        smoothedChannel_3 = knnForwardRegression(channel_3, 8)
        plt.plot(t, smoothedChannel_3, label = 'Channel_1 Signal (smoothed)')
        #plt.plot(t, channel_3, label = 'Channel_1 Signal')
        plt.xlabel('time')
        plt.ylabel('value')
        #plt.xlim(0, 600)
        plt.xlim(5660, 5930)
        plt.ylim(0, 1000)
        plt.legend()
        plt.show()