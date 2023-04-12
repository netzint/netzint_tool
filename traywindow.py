import sys
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QDesktopWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from niMaTracker import getStatusData
import json

class cssden(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # size
        self.setFixedSize(320, 450)
        self.center()
        statusData=json.loads(getStatusData())
        #print (type(statusData))
        for status in statusData:
            # label
            self.lbl = QLabel(self)
            self.lbl.setText(status)
            #self.lbl.setStyleSheet("background-color: rgb(0,0,0);"
            #                       "border: 1px solid red;"
            #                       "color: rgb(255,255,255);"
            #                       "font: bold italic 20pt 'Times New Roman';")
            #self.lbl.setGeometry(5, 5, 60, 40)

            self.show()

    # center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())
        self.move(1500, 0)
        # pybutton.move(110, 128)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.close()

    def close(self):
        self.close()


def displayWindow():
    app = QtWidgets.QApplication(sys.argv)
    preferences_window = cssden()
    preferences_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    displayWindow()