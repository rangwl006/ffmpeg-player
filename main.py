from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
import sys

from dashboard import Dashboard

if __name__=='__main__':
    # this declares the event loop
    # every qt application requires this line to get running
    app = QtWidgets.QApplication(sys.argv)

    # add all the components that need to be ran under this comment (usually its the main display)
    # in this case it is the videowidget
    videowidget = Dashboard()
    videowidget.show()

    # start the event loop
    app.exec()
