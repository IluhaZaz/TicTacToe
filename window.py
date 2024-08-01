import socket
import json
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep


with open("constants.json", mode = 'r', encoding = "utf-8") as f:
    const = json.load(f)


class GameWindow(QtWidgets.QMainWindow):
    def __init__(self, host, port) -> None:
        super().__init__()

        self.field: list[list[QtWidgets.QPushButton]] = [[], [], []]
        self.winner: str = None
        self.you: str = None
        self.opponent: str = None
        self.turn: str = 'X'
        self.moves_cnt: int = 0

        ui = Ui_MainWindow()
        ui.setupUi(self)

        self.client = None
        self.host = host
        self.port = port

        self.g_cycle_thread = GameCycleThread(self)
        self.loading_thread = LoadingThread(self, host, port)
    
    def create_connection(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, adress = server.accept()

        self.client = client
        self.you = 'X'
        self.opponent = 'O'

    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        self.client = client
        self.you = 'O'
        self.opponent = 'X'

    def move(self, x: int, y: int):
        if self.field[x][y].text() == '':
            self.field[x][y].setText(self.turn)
            self.moves_cnt += 1
            self.turn = self.opponent if self.turn == self.you else self.you
        self.winner = self.check_win()
        match(self.winner):
            case self.you:
                self.upLabel.setText("You win!")
            case "Tie":
                self.upLabel.setText("Tie")
            case self.opponent:
                self.upLabel.setText("You lose!")

    def cell_slot(self, x: int, y: int):
        if self.turn == self.you and not self.winner:
            self.move(x, y)
            self.client.send(pickle.dumps((x, y)))
    
    def check_win(self):
        for row in self.field:
            if row[0].text() == row[1].text() == row[2].text() != '':
                return row[0].text()
        for col in range(3):
            if self.field[0][col].text() == self.field[1][col].text() == self.field[2][col].text() != '':
                return self.field[0][col].text()
        if self.field[0][0].text() == self.field[1][1].text() == self.field[2][2].text() != '':
            return self.field[1][1].text()
        if self.field[0][2].text() == self.field[1][1].text() == self.field[2][0].text() != '':
            return self.field[1][1].text()
        if self.moves_cnt == 9:
            return "Tie"
        return None


class GameCycleThread(QtCore.QThread):
    def __init__(self, main_window: GameWindow) -> None:
        super().__init__()
        self.main_window = main_window

    def run(self):
        while self.main_window.winner is None:
            if self.main_window.client:
                if self.main_window.turn != self.main_window.you:
                    self.main_window.upLabel.setText("Opponent's turn")
                    move = self.main_window.client.recv(4096)
                    if move:
                        move = pickle.loads(move)
                        self.main_window.move(*move)
                else:
                    self.main_window.upLabel.setText("Your turn")
            sleep(0.5)
    

class LoadingThread(QtCore.QThread):
    def __init__(self, main_window: GameWindow, host, port) -> None:
        super().__init__()
        self.main_window = main_window
        self.host = host
        self.port = port

    def run(self):
        self.main_window.create_connection(self.host, self.port)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow: GameWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("TicTacToe")
        MainWindow.resize(800, 800)

        MainWindow.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.centralwidget.setObjectName("centralwidget")
        MainWindow.centralwidget.setStyleSheet("background: #B28B5C;"
                                                "border-left: 30px solid black;"
                                                "border-top: 30px solid black;"
                                                "border-left-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #B28B5C, stop: 1 #BF9F78);"
                                                "border-top-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #B28B5C, stop: 1 #BF9F78);"
                                                "border-right: 30px solid black;"
                                                "border-bottom: 30px solid black;"
                                                "border-right-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #A07A4B, stop: 1 #B28B5C);"
                                                "border-bottom-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #A07A4B, stop: 1 #B28B5C);"
                                               )

        MainWindow.upLabel = QtWidgets.QLabel(MainWindow.centralwidget)
        MainWindow.upLabel.setText("Waiting for oppenent")
        MainWindow.upLabel.setAlignment(QtCore.Qt.AlignCenter)
        MainWindow.upLabel.setGeometry(QtCore.QRect(175, round(0.4*const["CELL_SIZE"]), 
                                                     const["CELL_SIZE"]*3, round(0.5*const["CELL_SIZE"]))
                                        )
        MainWindow.upLabel.setStyleSheet("background: rgba(255, 255, 255, 0.1);"
                                         "border: 4px solid rgba(255, 255, 255, 0.2);"
                                         "font-size: 30px;"
                                         "color: rgba(0, 0, 0, 0.7);"
                                         )
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(63, 63, 63, 255))
        MainWindow.upLabel.setGraphicsEffect(shadow)

        MainWindow.gridLayoutWidget = QtWidgets.QWidget(MainWindow.centralwidget)
        MainWindow.gridLayoutWidget.setGeometry(QtCore.QRect(175, round(1.1*const["CELL_SIZE"]), const["CELL_SIZE"]*3, 
                                                             const["CELL_SIZE"]*3)
                                                )
        MainWindow.gridLayoutWidget.setObjectName("gridLayoutWidget")
        MainWindow.gridLayout = QtWidgets.QGridLayout(spacing = 0)
        MainWindow.gridLayoutWidget.setStyleSheet("border: 4px solid rgba(255, 255, 255, 0.1);")

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(63, 63, 63, 60))
        MainWindow.gridLayoutWidget.setGraphicsEffect(shadow)


        MainWindow.gridLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.gridLayout.setObjectName("gridLayout")

        MainWindow.gridLayoutWidget.setLayout(MainWindow.gridLayout)

        for i in range(3):
            for j in range(3):
                btn = QtWidgets.QPushButton(MainWindow.gridLayoutWidget)
                MainWindow.field[i].append(btn)
                MainWindow.gridLayout.addWidget(btn, i, j, 1, 1)
                btn.setFixedSize(const["CELL_SIZE"], const["CELL_SIZE"])
                btn.clicked.connect(lambda state, x = i, y = j: MainWindow.cell_slot(x, y))
                btn.setStyleSheet(
                    "background: rgba(255, 255, 255, 0.1);"
                    "color: rgba(255, 255, 255, 0.3);"
                    "font-size: 70px;"
                    "font-weight: bold;"
                )

        MainWindow.setCentralWidget(MainWindow.centralwidget)

