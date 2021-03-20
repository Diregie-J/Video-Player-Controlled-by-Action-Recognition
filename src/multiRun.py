import subprocess

subprocess.run("python realTimeReading.py & python videoPlayer.py & python resetResult.py", shell=True)

