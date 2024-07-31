import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from window import GameWindow


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = GameWindow("localhost", 9999)
    MainWindow.show()
    MainWindow.loading_thread.start()
    MainWindow.g_cycle_thread.start()
    sys.exit(app.exec_())