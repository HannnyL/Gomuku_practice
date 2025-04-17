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

r,t = "4,7".split(',')jsdk


print((int,r)+(int,t))

abc = "222"

print(int(abc)+1)

os.system('cls')

print("meile")
"""""
#先手/服务器决定棋盘大小 √  size应>10
#比分机制 √
#投降 √
#断线重连

import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要真的连接这个地址，只是触发底层分配本地地址
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # 获取失败时返回回环地址
    finally:
        s.close()
    return ip

print("本地局域网 IP:", get_local_ip())

