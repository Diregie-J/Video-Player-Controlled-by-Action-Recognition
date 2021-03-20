'''预览csv波形'''

import csv
from matplotlib import pyplot as plt
import numpy as np

def visFile(filename, visLength):
    with open(filename) as f:
        reader = csv.reader(f)

        channel_1 = []
        channel_2 = []
        channel_3 = []

        if visLength == 0:
            for row in reader:
                if len(row) != 3:
                    break
                ch_1 = float(row[0])
                ch_2 = float(row[1])
                ch_3 = float(row[2])
                channel_1.append(ch_1)
                channel_2.append(ch_2)
                channel_3.append(ch_3)
            visLength=range(0,len(channel_1))
        else:
            rowCount=0
            for row in reader:
                if len(row) != 3:
                    break
                if rowCount in visLength:
                    ch_1 = float(row[0])
                    ch_2 = float(row[1])
                    ch_3 = float(row[2])
                    channel_1.append(ch_1)
                    channel_2.append(ch_2)
                    channel_3.append(ch_3)
                rowCount+=1
                # if rowCount == visLength:
                #     break

    fig=plt.figure(dpi=128,figsize=(10,6))
    plt.plot(visLength,channel_1,c='red')
    plt.plot(visLength,channel_2,c='orange')
    plt.plot(visLength,channel_3,c='blue')

    plt.title(filename,fontsize=24)
    plt.xlabel('Samples',fontsize=24)
    plt.ylabel('Sensor Read',fontsize=16)
    plt.tick_params(axis='both',which='major',labelsize=16)
    # plt.imsave(filename[0:-4]+'.jpg',np.array(fig))



if __name__ == "__main__":
    # movement=['d','u','l','r','f']
    # movement=['fist']
    # for index in movement:
    #     for i in range(0,1):
    #         visFile(index+str(i)+'.csv')


    # visFile('./DataSet/newFromRealTime/hyqData/rr1_log.csv',0)
    # visFile('./DataSet/newFromRealTime/hyqData/rr2_log.csv',0)
    # visFile('./DataSet/newFromRealTime/hyqData/rr3_log.csv',0)
    visFile('DataSet/newFromRealTime/rr1.csv',0)
    visFile('DataSet/newFromRealTime/rw2.csv',0)
    # visFile('DataSet/newFromRealTime/rr3.csv',0)
    # visFile('./DataSet/newFromRealTime/rw1_log.csv',0)
    # visFile('./DataSet/newFromRealTime/rw2_log.csv',0)
    # visFile('./DataSet/newFromRealTime/rw3_log.csv',0)
    # visFile('./src/DataSet/newFromRealTime/hyqData/lrTrial1_log.csv',0)
    # visFile('./src/DataSet/newFromRealTime/hyqData/lrTrial2_log.csv',0)
    # visFile('./src/DataSet/newFromRealTime/hyqData/lrTrial3_log.csv',0)
    # visFile('./src/DataSet/newFromRealTime/sgfDataRL/lw.csv',range(3000,5000))
    # visFile('./src/DataSet/newFromRealTime/zjhData/lw.csv',range(3000,5000))
    
    plt.show()