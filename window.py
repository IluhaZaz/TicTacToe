import sys
import json

from PyQt5 import QtCore, QtGui, QtWidgets

from classes import Game

with open("constants.json", mode = 'r', encoding = "utf-8") as f:
    const = json.load(f)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow: QtWidgets.QMainWindow):

        self.game = Game()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("TicTacToe")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(140, 80, const["CELL_SIZE"]*3, const["CELL_SIZE"]*3))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(spacing = 0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayoutWidget.setLayout(self.gridLayout)

        self.field: list[QtWidgets.QPushButton] = []

        for i in range(9):
            btn = QtWidgets.QPushButton(self.gridLayoutWidget)
            self.field.append(btn)
            btn.setObjectName("pushButton")
            self.gridLayout.addWidget(btn, i//3, i%3, 1, 1)
            btn.setFixedSize(const["CELL_SIZE"], const["CELL_SIZE"])

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 40, 47, 14))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
