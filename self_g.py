
class Gomuku:
    
    def __init__(self,size):
        self.size = size
        self.board = [['·' for _ in range(size)] for _ in range(self.size)]



    def print_board(self,player):

        print("\n  " + " ".join([str(i) for i in range(self.size)])) #用.join可以消除中括号
        for idx,row in enumerate(self.board): #enumerate用来获取每行的索引idx，不然只能直接输出row内容
            print(f"{idx} "+" ".join(row))
        print("我方:O   对方:X") if player == 'O' else print("我方:X   对方:O")
        print() #用来添加空行


    def is_valid_move(self,x,y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == '·'


    def update_board(self,x,y,player):
        if self.is_valid_move(x,y):
            self.board[y][x] = player
            return True
        return False
    
    def win_check(self,x,y,player):
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dx,dy in directions:
            count = 1
            for dir in [1,-1]:
                for i in range(1,5):
                    nx = x + dir*dx*i
                    ny = y + dir*dy*i
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False



        


        
