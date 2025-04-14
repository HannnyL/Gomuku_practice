import self_g as game
import os
"""""
player = "X"

newgame = game.Gomuku(10)

newgame.print_board()

for i in range(2,7):
    newgame.update_board(i,i,player)

    newgame.print_board()

    if newgame.win_check(i,i,player):
        print("你赢啦")
        break


move = input("输入坐标")
nx,ny = [move[0],move[2]]
print(f"[]")

r,t = "4,7".split(',')

print((int,r)+(int,t))
"""""
#先手/服务器决定棋盘大小 √  size应>10
#比分机制 √
#投降 √
#断线重连
abc = "222"

print(int(abc)+1)

os.system('cls')

print("meile")