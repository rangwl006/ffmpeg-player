from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

# import our own modules
from videowidget import VideoWidget

class Dashboard(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Note: object variables that have the self.__[name] means that they are private
        # The user (if we give the code to other people, they should not be touching this at all) should not be able to see this
        # Private variables are usually used within the class only
        self.__windowTitle = "TITLE"
        self.__defaultSize = QtCore.QSize(1080,720)
        self.videowidget = VideoWidget()
        self.__setupMainWindow()

    def __setupMainWindow(self):
        self.__mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.__mainWidget)
        self.__mainWidgetLayout = QtWidgets.QVBoxLayout()
        self.__mainWidgetLayout.addWidget(self.videowidget)
        self.__mainWidget.setLayout(self.__mainWidgetLayout)


