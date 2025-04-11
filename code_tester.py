import self_g as game

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

"""""
r,t = "4,7".split(',')

print((int,r)+(int,t))