# game.py

class Gomoku:
    def __init__(self, size=10):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]

    def print_board(self):
        print("\n  " + " ".join([str(i) for i in range(self.size)]))
        for idx, row in enumerate(self.board):
            print(f"{idx} " + " ".join(row))
        print()

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == '.'

    def place_stone(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[y][x] = player
            return True
        return False

    def check_win(self, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for dir in [1, -1]:
                for i in range(1, 5):
                    nx = x + dx * i * dir
                    ny = y + dy * i * dir
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False
