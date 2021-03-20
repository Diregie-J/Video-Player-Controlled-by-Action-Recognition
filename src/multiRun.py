import subprocess

subprocess.run("python videoPlayer.py & python realTimeReading.py & python resetResult.py& ", shell=True)



# import sys
# import videoPlayer
# import resetResult
# import realTimeReading

# sys.modules['realTimeReading'].__dict__.clear()
# sys.modules['resetResult'].__dict__.clear()
# sys.modules['videoPlayer'].__dict__.clear()

# print('1')
# realTimeReading.py
# print('2')
# resetResult.py
# print('3')
# videoPlayer.py
# print('4')