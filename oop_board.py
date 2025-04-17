class Board:
    def __init__(self,size):
        self.size = size
        self.leftstep = size*size
        self.board = [['·' for _ in range(size)] for _ in range(size)]


    def print_board(self):
        if self.size <= 10:
            print("\nx→ " + " ".join([str(i) for i in range(self.size)]))
        else:
            print("\n\\x " + " ".join([str(int(i/10)) for i in range(self.size)]))          
            print("y\\ " + " ".join([str(int(i%10)) for i in range(self.size)])) 
        for idx,row in enumerate(self.board):
            if idx <= 9:
                print(f"0{idx} "+" ".join(row))
            else:
                print(f"{idx} "+" ".join(row))


    def is_valid_move(self,x,y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == '·'
    
    def update_board(self,x,y,piece):
        if self.is_valid_move(x,y):
            self.board[y][x] = piece
            self.leftstep -= 1
            return True
        else:
            return False

    def win_check(self,x,y,piece):
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dx,dy in directions:
            counter = 1            
            for dir in [1,-1]:
                for i in range(1,5):
                    nx = x + dir*i*dx
                    ny = y + dir*i*dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == piece:
                        counter += 1
                    else:
                        break
            if counter >= 5:
                return True                
        return False
