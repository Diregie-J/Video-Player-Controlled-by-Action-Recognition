'''预览csv波形'''

import csv
from matplotlib import pyplot as plt
import numpy as np

def visFile(filename):
    with open(filename) as f:
        reader = csv.reader(f)

        channel_1 = []
        channel_2 = []
        channel_3 = []

        for row in reader:
            if len(row) != 3:
                break
            ch_1 = float(row[0])
            ch_2 = float(row[1])
            ch_3 = float(row[2])
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
    # plt.imsave(filename[0:-4]+'.jpg',np.array(fig))



if __name__ == "__main__":
    # movement=['d','u','l','r','f']
    # movement=['fist']
    # for index in movement:
    #     for i in range(0,1):
    #         visFile(index+str(i)+'.csv')

    # visFile('./src/DataSet/newFromRealTime/sgfDataRL/rr.csv')
    visFile('./src/DataSet/newFromRealTime/hyqData/lrTrial2.csv')
    visFile('./src/DataSet/newFromRealTime/sgfDataRL/lr.csv')
    visFile('./src/DataSet/newFromRealTime/zjhData/lr.csv')
    # visFile('./src/rrTrial5.csv')
    # # visFile('./src/rrTrial6.csv')
    # visFile('./src/rrTrial4_log.csv')
    
    plt.show()