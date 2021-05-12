from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import numpy as np

from ffmpeg_thread import FfmpegWorker

class VideoWidget(QtWidgets.QWidget):

    def __init__(self):
        # initialise the superclass (in this case QWdiget)
        super().__init__()

        self.__ffmpegWorker = FfmpegWorker()
        self.__ffmpegWorker.tx_frame.connect(self.rx_processFrame)

        self.__defaultSize = QtCore.QSize(720,480)
        self.__layout = QtWidgets.QVBoxLayout()

        self.setFixedSize(self.__defaultSize)

        self.display = QtWidgets.QLabel()
        self.display.setFixedSize(QtCore.QSize(640,480))

        self.__layout.addWidget(self.display)
        
        self.setLayout(self.__layout)
        
    @pyqtSlot(np.ndarray)
    def rx_processFrame(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = width * 3
        img = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format.Format_RGB888)
        img_pixmap = QtGui.QPixmap.fromImage(img)
        self.display.setPixmap(img_pixmap)