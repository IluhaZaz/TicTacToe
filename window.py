import socket
import json

from PyQt5 import QtCore, QtGui, QtWidgets


with open("constants.json", mode = 'r', encoding = "utf-8") as f:
    const = json.load(f)


class GameWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
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
    
    def create_connection(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, adress = server.accept()

        self.client = client
        self.you = 'X'
        self.opponent = 'O'

        self.thread = GameWindowThread(self)

    def connect(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.client = client
        self.you = 'O'
        self.opponent = 'X'

        self.thread = GameWindowThread(self)

    def move(self, x: int, y: int):
        if self.field[x][y].text() == '':
            self.field[x][y].setText(self.turn)
            self.moves_cnt += 1
            self.turn = self.opponent if self.turn == self.you else self.you

    def cell_slot(self, x: int, y: int):
        if self.turn == self.you:
            self.move(x, y)
            m = f"{x} {y}"
            self.client.send(m.encode("utf-8"))
    
    def check_win(self):
        for row in self.field:
            if row[0].text() == row[1].text() == row[2].text() != '':
                return self.opponent
        for col in range(3):
            if self.field[0][col].text() == self.field[1][col].text() == self.field[2][col].text() != '':
                return self.opponent
        if self.field[0][0].text() == self.field[1][1].text() == self.field[2][2].text() != '':
            return self.opponent
        if self.field[0][2].text() == self.field[1][1].text() == self.field[2][0].text() != '':
            return self.opponent
        if self.moves_cnt == 9:
            return "Tie"
        return None


class GameWindowThread(QtCore.QThread):
    def __init__(self, main_window: GameWindow) -> None:
        super().__init__()
        self.main_window = main_window

    def run(self):
        while self.main_window.winner is None:
            if self.main_window.turn != self.main_window.you:
                move = self.main_window.client.recv(3)
                if move:
                    self.main_window.move(*list(map(int, move.decode("utf-8").split())))
            self.main_window.winner = self.main_window.check_win()
        match(self.main_window.winner):
            case self.main_window.you:
                print("You win!")
            case "Tie":
                print("Tie")
            case _:
                print("You lose!")
        self.main_window.client.close()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow: GameWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("TicTacToe")
        MainWindow.resize(800, 600)

        MainWindow.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.centralwidget.setObjectName("centralwidget")

        MainWindow.gridLayoutWidget = QtWidgets.QWidget(MainWindow.centralwidget)
        MainWindow.gridLayoutWidget.setGeometry(QtCore.QRect(140, 80, const["CELL_SIZE"]*3, const["CELL_SIZE"]*3))
        MainWindow.gridLayoutWidget.setObjectName("gridLayoutWidget")
        MainWindow.gridLayout = QtWidgets.QGridLayout(spacing = 0)
        MainWindow.gridLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.gridLayout.setObjectName("gridLayout")

        MainWindow.gridLayoutWidget.setLayout(MainWindow.gridLayout)

        for i in range(3):
            for j in range(3):
                btn = QtWidgets.QPushButton(MainWindow.gridLayoutWidget)
                MainWindow.field[i].append(btn)
                btn.setObjectName("pushButton")
                MainWindow.gridLayout.addWidget(btn, i, j, 1, 1)
                btn.setFixedSize(const["CELL_SIZE"], const["CELL_SIZE"])
                btn.clicked.connect(lambda state, x = i, y = j: MainWindow.cell_slot(x, y))

        MainWindow.setCentralWidget(MainWindow.centralwidget)

