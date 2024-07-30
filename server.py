import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from window import GameWindow


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = GameWindow()
    MainWindow.show()
    MainWindow.create_connection("localhost", 9999)
    MainWindow.thread.start()
    sys.exit(app.exec_())