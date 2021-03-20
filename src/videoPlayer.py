import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)

forwardLock = 0
backwardLock = 0
upLock = 0
downLock = 0

class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        iconSize = QSize(12, 12)
        videoWidget = QVideoWidget()

        openButton = QPushButton("Open Video")
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.setFont(QFont("Noto Sans", 10))
        openButton.clicked.connect(self.abrir)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(iconSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        #进度条
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)


        #音量条
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.sliderMoved.connect(self.setVolume)
        

        #Information bar
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.volumeChanged.connect(self.volumeChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")

    def abrir(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",
                ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        print("Play state:", state)
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        pause = False
        global forwardLock
        global backwardLock
        f = open("test.txt", "r+")
        data = f.readline()
        print("Reading txt...")
        print("Data read from txt: ", data)
        if data == "22":
            pause = True
            self.mediaPlayer.pause()
            self.mediaStateChanged(2)
            f.close()
            '''while pause:
                f = open("test.txt", "r+")
                l = f.readline()
                if l == "00":
                    pause = False
                    self.mediaPlayer.play()
                    self.mediaStateChanged(1)
                f.close()'''

        if data == "22" and forwardLock == 0:
            f.close()
            forwardLock = 1
            self.setPosition(position+20000)
        elif data != "22" and forwardLock == 1:
            forwardLock = 0
            f.close()
        else:
            f.close()

        
        if data == "22" and backwardLock == 0:
            f.close()
            backwardLock = 1
            if position > 20000:
                self.setPosition(position-20000)
            else:
                self.setPosition(0)
        elif data != "22" and backwardLock == 1:
            backwardLock = 0
            f.close()
        else:
            f.close()
        print("Position changed:", position)

    def volumeChanged(self, value):
        self.volumeSlider.setValue(value)
        global upLock
        global downLock
        f = open("test.txt", "r+")
        data = f.readline()

        if data == "33" and upLock == 0:
            f.close()
            upLock = 1
            if value+5 > 100:
                self.setVolume(100)
            else:
                self.setVolume(value + 5)
        elif data != "33" and upLock == 1:
            upLock = 0
            f.close()
        else:
            f.close()

        
        if data == "44" and downLock == 0:
            f.close()
            downLock = 1
            if value-5 < 0:
                self.setVolume(0)
            else:
                self.setVolume(value - 5)
        elif data != "44" and downLock == 1:
            downLock = 0
            f.close()
        else:
            f.close()
        

    def setVolume(self, value):
        self.mediaPlayer.setVolume(value)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        print("Duration changed:", duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        print("Position set:", position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.setWindowTitle("Player")
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
