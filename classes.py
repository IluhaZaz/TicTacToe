import socket


class Game:

    def __init__(self) -> None:
        self.field: list[list[int]] = [[' ' for _ in range(3)] for _ in range(3)]
        self.winner: str = None
        self.you: str = None
        self.turn = 'X'
    
    def create_connection(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, adress = server.accept()
        print("Game is started!")

        self.you = 'X'

        return client

    def connect(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print("Game is started!")

        self.you = 'O'
    
    def move(self, x: int, y: int):
        self.field[x][y] = self.turn
        self.turn = 'X' if self.turn == 'O' else 'O'