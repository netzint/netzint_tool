import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QTableWidget, QTableWidgetItem, QAction, QWidgetAction, QDialog, QMainWindow,QLabel, QDesktopWidget
from PyQt5.QtGui import QIcon
import traywindow
from PyQt5 import QtCore, QtWidgets, QtGui




class TrayIcon(QWidget):
    def __init__(self):
        super().__init__()
        self.window = None
        self.initUI()

    def showTimeClock(self):
        #widgets = QApplication.topLevelWidgets()
        self.window = traywindow.cssden()
        self.window.show()
        #print (widgets)
        #if self.window is not None and self.window.isVisible():
        #    self.window.close()
        #else:
        #    self.window = traywindow.cssden()
        #    self.window.show()

    def initUI(self):
        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))
        self.tray_icon.show()

        self.menu = QMenu(self)

        prefs_action = self.menu.addAction('Mitarbeiter')
        prefs_action.triggered.connect(self.showTimeClock)
        self.menu.addSeparator()
        self.quit_action = QAction('Quit', self)
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.quit_action)

        # Set the tray icon's context menu to the menu
        self.tray_icon.setContextMenu(self.menu)

    def quit(self):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tray_icon = TrayIcon()
    sys.exit(app.exec_())
