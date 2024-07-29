import socket


class Game:

    def __init__(self) -> None:
        self.field: list[list[int]] = [[' ' for _ in range(3)] for _ in range(3)]
        self.winner: str = None
        self.you: str = None
        self.turn = 'X'
        self.moves_cnt = 0
    
    def create_connection(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, adress = server.accept()
        print("Game is started!")

        self.you = 'X'

        self.start_game(client)
        server.close()

    def connect(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print("Game is started!")
        self.you = 'O'
        self.start_game(client)
        client.close()
    
    def move(self, x: int, y: int):
        self.field[x][y] = self.turn
        self.moves_cnt += 1
        self.turn = 'X' if self.turn == 'O' else 'O'

    def check_win(self):
        for row in self.field:
            if row[0] == row[1] == row[2] != ' ':
                return self.turn
        for col in range(3):
            if self.field[0][col] == self.field[1][col] == self.field[2][col] != ' ':
                return self.turn
        if self.field[0][0] == self.field[1][1] == self.field[2][2] != ' ':
            return self.turn
        if self.field[0][2] == self.field[1][1] == self.field[2][0] != ' ':
            return self.turn
        if self.moves_cnt == 9:
            return "Tie"
        return None
    
    def print_field(self):
        print(" _____ ")
        for row in self.field:
            print("|" + "|".join(row) + "|")
        print(" ‾‾‾‾‾ ")

    def start_game(self, client):
        while self.winner is None:
            if self.turn == self.you:
                move: str = input("Enter your move position like 'x y'")
                pos: list[int] = list(map(int, move.split()))
                self.move(*pos)
                client.send(move.encode("utf-8"))
            else:
                move = client.recv(3)
                self.move(*list(map(int, move.decode("utf-8").split())))
            self.print_field()
            self.winner = self.check_win()
        match(self.winner):
            case self.you:
                print("You win!")
            case "Tie":
                print("Tie")
            case _:
                print("You lose!")
